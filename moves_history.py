import time
from copy import deepcopy
from heapq import *
import random
from board import *
from game import print_game_comfortably
from utils import F_OUTPUT_A_STAR_FILE


class GameState:

    def __init__(self, priority, car_name, steps, direction, prev_state, actual_game, num_of_moves_to_get_to_state):
        self.priority = priority
        self.car_name = car_name
        self.steps = steps
        self.direction = direction
        self.actual_game: Board = actual_game
        self.prev_state = prev_state
        self.num_of_moves_to_get_to_state = num_of_moves_to_get_to_state

    def __eq__(self, other):
        return other.actual_game.game_board_as_string == self.actual_game.game_board_as_string
    # TODO: Careful here, maybe it messed things up (the equation with game_board_as_string, previously: gameboard

    def __lt__(self, other):
        return self.priority < other.priority

    # def __hash__(self):
    #     return hash(self.actual_game)

class AStarAlgorithm:
    def __init__(self, actual_game: Board, heuristic_function, timer, game_number):
        self.searched_nodes = 0
        self.total_heuristic = 0
        self.expand_number = 0
        self.game_number = game_number
        self.timer = timer
        self.heuristic_function = heuristic_function
        self.start_time = time.time()
        self.closed = {}
        self.open = []
        self.hash_for_open = {}
        # also initial state:
        red_car_info = actual_game.cars_information.get("X")
        self.current_state = self.translate_board_to_state(actual_game, red_car_info)
        self.actual_game: Board = actual_game
        self.closed[self.actual_game.game_board_as_string] = self.current_state
        list = self.expand()
        for state in list:
            self.hash_for_open[state.actual_game.game_board_as_string] = state
            heappush(self.open, state)
        self.algorithm()

    def translate_board_to_state(self, actual_game: Board, red_car_info: Car):
        return GameState(self.evaluate_initial_fn(actual_game.game_board, red_car_info.end_col), None, None, None, None, actual_game, 0)

    # wrapper function, do not call unless in evaluate_fn
    @staticmethod
    def evaluate_initial_fn(game_board, red_car_end_col):
        counter = 0
        for i in range(red_car_end_col + 1, 6):
            if game_board[2][i] != '.':
                counter += 1
        return counter

    # expands the current state
    def expand(self):
        self.expand_number += 1
        state_list = []
        for car_name in self.actual_game.cars_information.keys():
            current_car_info: Car = self.actual_game.cars_information.get(car_name)
            state_list_per_car = self.generate_state_for_all_possible_moves(car_name, current_car_info)
            state_list += state_list_per_car
        # self.searched_nodes += len(state_list)
        return state_list

    def generate_state_for_all_possible_moves(self, car_name, car_information: Car):
        red_car_end_col = self.actual_game.cars_information.get("X").end_col
        if car_information.direction == Direction.ROW:
            return self.get_game_states_in_row(car_name, red_car_end_col)
        elif car_information.direction == Direction.COL:
            return self.get_game_states_in_col(car_name, car_information, red_car_end_col)
        raise Exception("Incorrect Direction in generate_state_for_all_possible_moves")

    def get_game_states_in_row(self, car_name, red_car_end_col):
        list_states = []
        for i in range(4):
            if self.actual_game.is_legal_move(car_name, i):
                priority = self.infer_priority_by_heuristic_function(Direction.ROW, -1, -1, -1)
                board_copy = self.actual_game.copy_me()
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(priority, car_name, i, MoveDirection.RIGHT, self.current_state, board_copy, self.current_state.num_of_moves_to_get_to_state + 1))
        for i in range(-4, 0):
            if self.actual_game.is_legal_move(car_name, i):
                priority = self.infer_priority_by_heuristic_function(Direction.ROW, -1, -1, -1)
                board_copy = self.actual_game.copy_me()
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(priority, car_name, abs(i), MoveDirection.LEFT, self.current_state, board_copy, self.current_state.num_of_moves_to_get_to_state + 1))
        return list_states

    def get_game_states_in_col(self, car_name, car_information, red_car_end_col):
        list_states = []
        for i in range(4):
            if self.actual_game.is_legal_move(car_name, i):
                priority = self.infer_priority_by_heuristic_function(Direction.COL, car_information, red_car_end_col, i)
                board_copy = self.actual_game.copy_me()
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(priority, car_name, i, MoveDirection.DOWN, self.current_state, board_copy, self.current_state.num_of_moves_to_get_to_state + 1))
        for i in range(-4, 0):
            if self.actual_game.is_legal_move(car_name, i):
                priority = self.infer_priority_by_heuristic_function(Direction.COL, car_information, red_car_end_col, i)
                board_copy = self.actual_game.copy_me()
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(priority, car_name, abs(i), MoveDirection.UP, self.current_state, board_copy, self.current_state.num_of_moves_to_get_to_state + 1))
        return list_states

    def infer_priority_by_heuristic_function(self, direction, car_information, red_car_end_col, steps):
        if self.heuristic_function == 1:
            return self.heuristic_function1(direction, car_information, red_car_end_col, steps)
        elif self.heuristic_function == 2:
            return self.heuristic_function2()
        elif self.heuristic_function == 4:
            return self.heuristic_function4()
        elif self.heuristic_function == 5:
            return self.heuristic_function5(car_information, red_car_end_col)
        elif self.heuristic_function == 6:
            return self.heuristic_function6(car_information, red_car_end_col)
        elif self.heuristic_function == 10:
            return self.heuristic_function6(car_information, red_car_end_col)* self.heuristic_function5(car_information, red_car_end_col)
        else:
            raise Exception('got a wrong HEURISTIC function number!!{}'.format(self.heuristic_function))

    def heuristic_function1(self, direction, car_information, red_car_end_col, steps):
        if direction == Direction.ROW:
            value = 0
        else:
            value = self.get_priority(car_information, red_car_end_col, steps)
        return value + 1 + self.current_state.priority

    def heuristic_function2(self):
        self.current_state.num_of_moves_to_get_to_state + self.get_num_of_blocked_cars_on_red_row(0)

    def heuristic_function4(self):
        return self.get_num_of_blocked_cars_on_red_row(self.actual_game.red_car_info.end_col+1)

    def get_num_of_blocked_cars_on_red_row(self, start_col):
        counter = 0
        for i in range(start_col, 6):
            curr_car_name = self.actual_game.game_board[2][i]
            if curr_car_name == '.' or curr_car_name == 'X':
                continue
            if self.is_column_car_blocked(curr_car_name, i):
                counter += 1
        return counter

    def is_column_car_blocked(self, car_name, col):
        car_info: Car = self.actual_game.cars_information[car_name]
        # moving up
        if self.actual_game.is_legal_move(car_name, -1):
            start_row, end_row, _, _ = car_info.expected_location_after_move(MoveDirection.UP, 1)
            if end_row < 2:
                return False
        if self.actual_game.is_legal_move(car_name, -2):
            start_row, end_row, _, _ = car_info.expected_location_after_move(MoveDirection.UP, 2)
            if end_row < 2:
                return False
        if self.actual_game.is_legal_move(car_name, -3):
            start_row, end_row, _, _ = car_info.expected_location_after_move(MoveDirection.UP, 3)
            if end_row < 2:
                return False
        # moving down
        if self.actual_game.is_legal_move(car_name, 1):
            start_row, end_row, _, _ = car_info.expected_location_after_move(MoveDirection.DOWN, 1)
            if start_row > 2:
                return False
        if self.actual_game.is_legal_move(car_name, 2):
            start_row, end_row, _, _ = car_info.expected_location_after_move(MoveDirection.DOWN, 2)
            if start_row > 2:
                return False
        if self.actual_game.is_legal_move(car_name, 3):
            start_row, end_row, _, _ = car_info.expected_location_after_move(MoveDirection.DOWN, 3)
            if start_row > 2:
                return False
        return True

    @staticmethod
    def get_priority(car_information: Car, red_car_end_col, steps):
        if red_car_end_col > car_information.start_col:
            return 0
        final_start_row = car_information.start_row + steps
        final_end_row = car_information.end_row + steps
        car_was_near_line_3 = 2 in range(car_information.start_row, car_information.end_row + 1)
        car_will_be_near_line_3 = 2 in range(final_start_row, final_end_row + 1)
        if car_was_near_line_3 and not car_will_be_near_line_3:
            return -1
        elif not car_was_near_line_3 and car_will_be_near_line_3:
            return 1
        return 0

    def algorithm(self):
        # heappush(self.open, self.current_state)
        steps_so_far = 0
        while self.open:
            if time.time() - self.start_time >= self.timer:
                f = open(F_OUTPUT_A_STAR_FILE, "a")
                f.write("\nGame number{}, FAILED \n".format(self.game_number))
                break
            curr_min_state: GameState = heappop(self.open)
            list_for_min_states = [curr_min_state]
            if self.check_winning(curr_min_state.actual_game):
                self.searched_nodes += len(self.open) + len(self.closed)
                self.print_steps(curr_min_state)
                break
            flag = False
            while 1:
                # if heap becomes empty, stop looping:
                if not self.open:
                    break
                curr_min_priority_in_heap = self.open[0].priority
                if curr_min_priority_in_heap != curr_min_state.priority:
                    break
                another_min_state = heappop(self.open)
                if self.check_winning(another_min_state.actual_game):
                    self.searched_nodes += len(self.open) + len(self.closed)
                    self.print_steps(another_min_state)
                    flag = True
                    break
                list_for_min_states.append(another_min_state)
            if flag:
                break

            index = random.randint(0, len(list_for_min_states) - 1)
            curr_min_state = list_for_min_states[index]
            # here we didn't got our goal yet so we deal only with a one state so we push the rest
            for i in range(0, len(list_for_min_states)):
                if i == index:
                    continue
                heappush(self.open, list_for_min_states[i])


            # switch game board
            # TODO: Optimize initializing of Board every loop
            self.actual_game = curr_min_state.prev_state.actual_game.copy_me()  # TODO: Do we need deep copy?

            # add the min state to closed hash
            self.actual_game.move_car(curr_min_state.car_name, curr_min_state.direction, curr_min_state.steps)
            self.closed[self.actual_game.game_board_as_string] = curr_min_state
            self.current_state = curr_min_state


            # expand the min gameState
            steps_so_far += 1
            list_for_expand = self.expand()

            for state in list_for_expand:
                self.total_heuristic += state.priority
                # index_for_state_in_open = self.does_it_exist_in_open(state)
                state_in_open: GameState = self.hash_for_open.get(state.actual_game.game_board_as_string)
                exists_in_open = state_in_open is not None
                # copy_of_board: Board = deepcopy(self.actual_game)
                self.actual_game.move_car(state.car_name, state.direction, state.steps)
                state_in_closed: GameState = self.closed.get(self.actual_game.game_board_as_string)
                exists_in_closed: bool = state_in_closed is not None
                # state.prev_state = curr_min_state
                if not exists_in_closed and not exists_in_open:
                    state.prev_state = curr_min_state
                    self.hash_for_open[state.actual_game.game_board_as_string] = state
                    heappush(self.open, state)
                elif exists_in_closed:
                    if state_in_closed.priority > state.priority:
                        self.closed.pop(self.actual_game.game_board_as_string)
                        self.hash_for_open[state.actual_game.game_board_as_string] = state
                        heappush(self.open, state)
                else:
                    if state_in_open.priority > state.priority:
                        self.open.remove(state_in_open)
                        self.hash_for_open[state.actual_game.game_board_as_string] = state
                        heappush(self.open, state)
                self.actual_game.move_car(state.car_name, self.get_opp_side(state.direction), state.steps)

    def does_it_exist_in_open(self, state: GameState):
        open_length: int = len(self.open)
        for i in range(open_length):
            if state == self.open[i]:
                return i
        return -1

    @staticmethod
    def check_winning(copy_of_game_board: Board):
        red_car_end_col = copy_of_game_board.cars_information.get('X').end_col
        range_index = 6 - red_car_end_col
        for i in range(1, range_index):
            if copy_of_game_board.game_board[2][red_car_end_col + i] != '.':
                return False
        return True

    def print_steps(self, another_min_state: GameState):
        list_of_steps = []
        steps_to_get_red_out = 6 - another_min_state.actual_game.red_car_info.end_col + 1
        # list_of_steps.append("XR{}".format(steps_to_get_red_out))
        while another_min_state.prev_state is not None:
            list_of_steps.append(self.get_step_in_str(another_min_state))
            another_min_state = another_min_state.prev_state
        list_of_steps.reverse()
        # print(list_of_steps)
        f = open(F_OUTPUT_A_STAR_FILE, "a")
        f.write("\nGame number{}, Steps: ".format(self.game_number))
        j = 0
        for i in range(len(list_of_steps)):
            if j == 10:
                j = 0
                f.write('\n')
                f.write('                     ')
            j += 1
            f.write("{} ".format(list_of_steps[i]))
        f.write('\ntime: {} .'.format(time.time()-self.start_time))
        f.write('.\n              ')
        # self.print_board_after_doing_all_steps(list_of_steps, another_min_state, self.game_number)
        # f.write('\n')

    @staticmethod
    def get_step_in_str(prev_state: GameState):
        if prev_state.direction == MoveDirection.UP:
            return "{}U{}".format(prev_state.car_name, prev_state.steps)
        if prev_state.direction == MoveDirection.DOWN:
            return "{}D{}".format(prev_state.car_name, prev_state.steps)
        if prev_state.direction == MoveDirection.LEFT:
            return "{}L{}".format(prev_state.car_name, prev_state.steps)
        if prev_state.direction == MoveDirection.RIGHT:
            return "{}R{}".format(prev_state.car_name, prev_state.steps)

    def print_board_after_doing_all_steps(self, list_of_steps, another_min_state: GameState, game_number):
        # TODO: Optimize Printing
        print("\nGame number{}: ".format(self.game_number))
        tmp_board: Board = another_min_state.actual_game
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
        print(time.time()-self.start_time)
        print_game_comfortably(tmp_board)

    def heuristic_function5(self, car_information, red_car_end_col):
        sum_of_moves = 0
        for car in self.actual_game.cars_information.values():
            if car.direction == Direction.ROW:
                continue
            if car.end_col < red_car_end_col:
                continue
            if car.length == 2:
                sum_of_moves += 1
            else:
                sum_of_moves += 5 - car.end_row
        return sum_of_moves

    def heuristic_function6(self, car_information, red_car_end_col):
        sum_of_moves = 0
        for car in self.actual_game.cars_information.values():
            if car.direction == Direction.ROW:
                continue
            if car.end_col < red_car_end_col:
                continue
            if 2 in range(car.start_row, car.end_row):
                if car.length == 3:
                    for j in range(3, 6):
                        if self.actual_game.game_board[car.end_col][j] != '.':
                            sum_of_moves += 1
                else:
                    for i in range(3):
                        if self.actual_game.game_board[car.end_col][i] != '.':
                            sum_of_moves += 1
        return sum_of_moves

    @staticmethod
    def get_opp_side(moveDir: MoveDirection):
        if moveDir == MoveDirection.RIGHT:
            return MoveDirection.LEFT
        if moveDir == MoveDirection.LEFT:
            return MoveDirection.RIGHT
        if moveDir == MoveDirection.UP:
            return MoveDirection.DOWN
        if moveDir == MoveDirection.DOWN:
            return MoveDirection.UP
