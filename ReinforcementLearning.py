import random
from board import Board, MoveDirection, Car, Direction
from copy import deepcopy
import time
from utils import F_OUTPUT_REINFORCEMENT_FILE, INFINITY

ATTEMPTS_AMOUNT = 10


class GameAction:

    def __init__(self, car_name: str, direction: MoveDirection, steps: int, weight: int):
        self.car_name = car_name
        self.move_direction: MoveDirection = direction
        self.steps = steps
        self.weight = weight

    def __eq__(self, other):
        return self.car_name == other.car_name and self.steps == other.steps\
               and self.move_direction == other.move_direction

    def __hash__(self):
        return hash((self.car_name, self.move_direction, self.steps))

    def __str__(self):
        return '{}{}{}'.format(self.car_name, self.move_direction, self.steps)


class ReinforcementGameNode:

    def __init__(self, board: Board, car_name, direction, steps, weight, parent_node):
        self.action: GameAction = GameAction(car_name, direction, steps, weight)
        self.board_after_action: Board = board
        self.parent = parent_node

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
        # self.print_board_after_doing_all_steps(list_of_steps, node, game_index)
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
        f.write("total time{}\n".format(game_time))
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
            tmp_board.move_car(move[0], move_side,ord(move[2])-ord('0'))
        # print(time.time()-start_time)
        self.print_game_comfortably(tmp_board)

    @staticmethod
    def print_game_comfortably(game):
        for line in game.game_board:
            print(" ".join(line))
        print()

    # expands the current state
    def get_a_random_max_child(self, seen_game_actions):
        state_list = []
        for car_name in self.board_after_action.cars_information.keys():
            current_car_info: Car = self.board_after_action.cars_information.get(car_name)
            state_list_per_car = self.generate_state_for_all_possible_moves(car_name, current_car_info, seen_game_actions)
            state_list += state_list_per_car

        max_weight = max(state.action.weight for state in state_list)
        max_list = []
        for state in state_list:
            if state.action.weight == max_weight:
                max_list.append(state)

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
            if self.board_after_action.is_legal_move(car_name, i):
                board_copy = deepcopy(self.board_after_action)
                board_copy.do_the_move(car_name, i)
                new_node = ReinforcementGameNode(board_copy, car_name, MoveDirection.RIGHT, i, 0, self)
                list_states.append(self.get_new_node_initialized_correctly(new_node, seen_game_actions))
        for i in range(-4, 0):
            if self.board_after_action.is_legal_move(car_name, i):
                board_copy = deepcopy(self.board_after_action)
                board_copy.do_the_move(car_name, i)
                new_node = ReinforcementGameNode(board_copy, car_name, MoveDirection.LEFT, -i, 0, self)
                list_states.append(self.get_new_node_initialized_correctly(new_node, seen_game_actions))

        return list_states

    def get_game_states_in_col(self, car_name, seen_game_actions):
        list_states = []
        for i in range(4):
            if self.board_after_action.is_legal_move(car_name, i):
                board_copy = deepcopy(self.board_after_action)
                board_copy.do_the_move(car_name, i)
                new_node = ReinforcementGameNode(board_copy, car_name, MoveDirection.DOWN, i, 0, self)
                list_states.append(self.get_new_node_initialized_correctly(new_node, seen_game_actions))

        for i in range(-4, 0):
            if self.board_after_action.is_legal_move(car_name, i):
                board_copy = deepcopy(self.board_after_action)
                board_copy.do_the_move(car_name, i)
                new_node = ReinforcementGameNode(board_copy, car_name, MoveDirection.UP, -i, 0, self)
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

    def __init__(self, board: Board, optimal_solution, game_index: int, allocated_time: int, start_time):
        self.score = 0
        self.optimal_solution_actions = optimal_solution
        self.seen_game_actions = {}
        self.stack = list()
        self.current_time = 0
        self.shortest_path = None
        self.current_shortest_output_length = INFINITY
        # TODO: Add time element
        for i in range(ATTEMPTS_AMOUNT):
            self.stack.clear()
            win_node, is_path_shorter = self.learning_algorithm(board)
            if is_path_shorter:
                self.shortest_path = win_node

        if self.shortest_path is not None:
            self.current_time = self.shortest_path.print_steps_reinforcement(game_index, start_time)
        else:
            f = open(F_OUTPUT_REINFORCEMENT_FILE, "a")
            f.write("\nGame number{}: FAILED".format(game_index))
            print("Could not find solution!")

    def learning_algorithm(self, board):
        head: ReinforcementGameNode = ReinforcementGameNode(board, None, None, None, 0, None)
        if head.is_win_node():
            return head

        self.stack.append(head)

        while self.stack:
            current_node: ReinforcementGameNode = self.stack.pop()

            preferred_child: ReinforcementGameNode = current_node.get_a_random_max_child(self.seen_game_actions)

            if preferred_child.is_win_node():
                path_length = len(self.stack)
                if path_length < self.current_shortest_output_length:
                    self.current_shortest_output_length = path_length
                return preferred_child, True

            self.update_weights_of_child(preferred_child)
            self.stack.append(preferred_child)

        return None, False

    def update_weights_of_child(self, child: ReinforcementGameNode):
        delta = 0
        if self.seen_game_actions.get(child) is None:
            self.seen_game_actions[child] = child.action.weight
        else:
            delta -= 1

        if self.optimal_solution_actions.get(child) is not None:
            delta += 1

        self.seen_game_actions[child] += delta
