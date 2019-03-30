import random
from math import pow
import time
from copy import deepcopy

from board import Board, MoveDirection, Car, Direction
from utils import F_OUTPUT_REINFORCEMENT_FILE, INFINITY

ATTEMPTS_AMOUNT = 30
ACCEPTABLE_MOVE_THRESHOLD = 50


class GameAction:

    def __init__(self, car_name: str, direction: MoveDirection, steps: int, weight: int, step_index: int):
        self.car_name = car_name
        self.move_direction: MoveDirection = direction
        self.steps = steps
        self.weight = weight
        self.step_index = step_index

    def __eq__(self, other):
        return self.car_name == other.car_name and self.steps == other.steps\
               and self.move_direction == other.move_direction\
               and self.step_index == other.step_index

    def __hash__(self):
        return hash((self.car_name, self.move_direction, self.steps))

    def __str__(self):
        return '{}{}{}'.format(self.car_name, self.move_direction, self.steps)


class ReinforcementGameNode:

    def __init__(self, board: Board, car_name, direction, steps, weight, step_index, parent_node):
        self.action: GameAction = GameAction(car_name, direction, steps, weight, step_index)
        self.board_after_action: Board = board
        self.parent = parent_node

    def __eq__(self, other):
        return self.board_after_action.game_board_as_string == other.board_after_action.game_board_as_string

    def __hash__(self):
        return hash(self.board_after_action.game_board_as_string)

    def is_head(self):
        return self.parent is None

    def is_win_node(self):
        red_car_end_col = self.board_after_action.cars_information.get('X').end_col
        range_index = 6 - red_car_end_col
        for i in range(1, range_index):
            if self.board_after_action.game_board[2][red_car_end_col + i] != '.':
                return False
        return True

    def print_steps_reinforcement(self, game_index, start_time):
        list_of_steps = []
        node = self
        while not node.is_head():
            list_of_steps.append(node.action.__str__())
            node = node.parent
        list_of_steps.reverse()
        # print(list_of_steps)
        self.print_board_after_doing_all_steps(list_of_steps, node, game_index)
        f = open(F_OUTPUT_REINFORCEMENT_FILE, "a")
        f.write("\nGame number{}, Steps: ".format(game_index))
        j = 0
        for i in range(len(list_of_steps)):
            if j == 10:
                j = 0
                f.write('\n')
                f.write('                     ')
            j += 1
            f.write("{} ".format(list_of_steps[i]))
        f.write('.\n              ')
        game_time = time.time() - start_time
        f.write("total time (with all attempts accounted for): {}\n".format(game_time))
        return game_time

    def print_board_after_doing_all_steps(self, list_of_steps, another_min_state, game_number):
        # TODO: Optimize Printing
        print("\nGame number{}: ".format(game_number))
        tmp_board: Board = another_min_state.board_after_action
        for move in list_of_steps:
            move_side = MoveDirection.UP
            _move = move[1]
            if _move == 'D':
                move_side = MoveDirection.DOWN
            elif _move == 'L':
                move_side = MoveDirection.LEFT
            elif _move == 'R':
                move_side = MoveDirection.RIGHT
            tmp_board.move_car(move[0], move_side, ord(move[2])-ord('0'))
        # print(time.time()-start_time)
        self.print_game_comfortably(tmp_board)

    @staticmethod
    def print_game_comfortably(game):
        for line in game.game_board:
            print(" ".join(line))
        print()

    # expands the current state
    def get_a_random_max_child(self, seen_game_actions, hashed_path, seen_nodes):
        state_list = []
        for car_name in self.board_after_action.cars_information.keys():
            current_car_info: Car = self.board_after_action.cars_information.get(car_name)
            state_list_per_car = self.generate_state_for_all_possible_moves(car_name, current_car_info, seen_game_actions)
            state_list += state_list_per_car

        max_list = []
        while True:
            to_remove = []
            max_weight = max(state.action.weight for state in state_list)
            for state in state_list:
                if state.action.weight == max_weight:
                    if hashed_path.get(state) is None:
                        max_list.append(state)
                    else:
                        to_remove.append(state)

            for remove_state in to_remove:
                state_list.remove(remove_state)

            if max_list or not state_list:
                break

        if not max_list:
            return None

        return max_list[random.randint(0, len(max_list) - 1)]

    def generate_state_for_all_possible_moves(self, car_name, car_information: Car, seen_game_actions):
        if car_information.direction == Direction.ROW:
            return self.get_game_states_in_row(car_name, seen_game_actions)
        elif car_information.direction == Direction.COL:
            return self.get_game_states_in_col(car_name, seen_game_actions)
        raise Exception("Incorrect Direction in generate_state_for_all_possible_moves")

    def get_game_states_in_row(self, car_name, seen_game_actions):
        list_states = []
        for i in range(4):
            move = 4 - i
            if self.board_after_action.is_legal_move(car_name, move):
                board_copy = deepcopy(self.board_after_action)
                board_copy.do_the_move(car_name, move)
                new_node = ReinforcementGameNode(board_copy, car_name, MoveDirection.RIGHT, move, 0, self.action.step_index + 1, self)
                list_states.append(self.get_new_node_initialized_correctly(new_node, seen_game_actions))
        for i in range(-4, 0):
            if self.board_after_action.is_legal_move(car_name, i):
                board_copy = deepcopy(self.board_after_action)
                board_copy.do_the_move(car_name, i)
                new_node = ReinforcementGameNode(board_copy, car_name, MoveDirection.LEFT, -i, 0, self.action.step_index + 1, self)
                list_states.append(self.get_new_node_initialized_correctly(new_node, seen_game_actions))

        return list_states

    def get_game_states_in_col(self, car_name, seen_game_actions):
        list_states = []
        for i in range(4):
            if self.board_after_action.is_legal_move(car_name, i):
                board_copy = deepcopy(self.board_after_action)
                board_copy.do_the_move(car_name, i)
                new_node = ReinforcementGameNode(board_copy, car_name, MoveDirection.DOWN, i, 0, self.action.step_index + 1, self)
                list_states.append(self.get_new_node_initialized_correctly(new_node, seen_game_actions))

        for i in range(-4, 0):
            if self.board_after_action.is_legal_move(car_name, i):
                board_copy = deepcopy(self.board_after_action)
                board_copy.do_the_move(car_name, i)
                new_node = ReinforcementGameNode(board_copy, car_name, MoveDirection.UP, -i, 0, self.action.step_index + 1, self)
                list_states.append(self.get_new_node_initialized_correctly(new_node, seen_game_actions))

        return list_states

    @staticmethod
    def get_new_node_initialized_correctly(new_node, seen_game_actions):
        weight = seen_game_actions.get(new_node.action)
        if weight is None:
            weight = 0
        new_node.action.weight = weight
        return new_node


class ReinforcementLearning:

    @staticmethod
    def allocated_time_per_attempt(allocated_total_time, game_index):
        initial_limit = min(allocated_total_time, pow(2, 6))
        limit = initial_limit
        allocated_times = []
        current_time = pow(2, 0)
        for i in range(ATTEMPTS_AMOUNT-1):
            if current_time >= limit:
                current_time = pow(2, 0)
            # allocated_times += [float(allocated_total_time)/float(ATTEMPTS_AMOUNT)]
            allocated_times += [current_time]
            limit -= current_time
            current_time *= 2.0
        # for i in range(len(allocated_times), ATTEMPTS_AMOUNT):
        #     allocated_times += [current_time]
        used_time = sum(allocated_times)
        last_time = 0
        if used_time < allocated_total_time:
            last_time = allocated_total_time - used_time
        allocated_times += [last_time]
        print("Game {}: sum of times = {}, all times = {}".format(game_index, sum(allocated_times), allocated_times))
        return allocated_times

    def __init__(self, board: Board, optimal_solution, game_index: int, allocated_time: int):
        self.optimal_solution_actions = optimal_solution
        self.seen_game_actions = {}
        self.already_seen_nodes = {}
        self.stack = list()
        self.current_time = 0
        self.shortest_path = None
        self.current_shortest_output_length = INFINITY
        allocated_time_per_attempt = self.allocated_time_per_attempt(allocated_time, game_index)
        start_time = time.time()
        for i in range(ATTEMPTS_AMOUNT):
            self.stack.clear()
            self.already_seen_nodes.clear()
            win_node, is_path_shorter, remaining_time = self.learning_algorithm(board, allocated_time_per_attempt[i])
            allocated_time_per_attempt[-1] += remaining_time
            if is_path_shorter:
                self.shortest_path = win_node
            if self.current_shortest_output_length <= ACCEPTABLE_MOVE_THRESHOLD:
                break

        if self.shortest_path is not None:
            self.current_time = self.shortest_path.print_steps_reinforcement(game_index, start_time)
        else:
            f = open(F_OUTPUT_REINFORCEMENT_FILE, "a")
            f.write("\nGame number{}: FAILED IN ALLOCATED TIME {} per attempt (total attempts = {})\n".format(game_index, allocated_time_per_attempt, ATTEMPTS_AMOUNT))
            self.current_time = time.time() - start_time

    # this function returns True if the algorithm has been trying to solve for too long
    # otherwise, it returns False, alongside the remainder of time it should be allowed to try again
    @staticmethod
    def exceeded_allowed_time(run_start_time, allowed_time):
        now = time.time()
        passed_time = now - run_start_time
        if passed_time >= allowed_time:
            return True, 0
        return False, allowed_time - passed_time

    def learning_algorithm(self, board, allowed_time):
        run_start_time = time.time()
        remaining_time = 0
        should_stop = False

        head: ReinforcementGameNode = ReinforcementGameNode(board, None, None, None, 0, -1, None)
        if head.is_win_node():
            return head

        self.stack.append(head)
        hashed_stack = {head: head}
        while self.stack:
            should_stop, remaining_time = self.exceeded_allowed_time(run_start_time, allowed_time)
            if should_stop:
                break

            current_node: ReinforcementGameNode = self.stack.pop()
            hashed_stack[current_node] = None
            if hashed_stack.get(current_node) is not None:
                continue

            # if self.already_seen_nodes.get(current_node.board_after_action.game_board_as_string) is not None:
            #     continue
            # self.already_seen_nodes[current_node.board_after_action.game_board_as_string] = 1

            preferred_child: ReinforcementGameNode = current_node.get_a_random_max_child(self.seen_game_actions, hashed_stack, self.already_seen_nodes)

            if preferred_child is None:
                continue
            elif preferred_child.is_win_node():
                is_shorter = False
                path_length = len(self.stack)
                if path_length < self.current_shortest_output_length:
                    self.current_shortest_output_length = path_length
                    is_shorter = True
                return preferred_child, is_shorter, remaining_time

            self.update_weights_of_child(preferred_child)
            self.stack.append(preferred_child)
            hashed_stack[preferred_child] = preferred_child

        return None, False, remaining_time

    def update_weights_of_child(self, node: ReinforcementGameNode):
        delta = 0
        if self.seen_game_actions.get(node.action) is None:
            self.seen_game_actions[node.action] = node.action.weight
        else:
            delta -= 1

        if self.optimal_solution_actions.get(node.action) is not None:
            delta += 1

        self.seen_game_actions[node.action] += delta
