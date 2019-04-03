import random
import sys

from board import *
from copy import deepcopy
from heapq import *
from utils import F_OUTPUT_DOUBLE_A_STAR_FILE
import time

class GameState:

    def __init__(self, priority, car_name, steps, direction, prev_state, actual_game, num_of_moves_to_get_to_state, depth):
        self.priority = priority
        self.car_name = car_name
        self.steps = steps
        self.direction = direction
        self.actual_game: Board = actual_game
        self.prev_state = prev_state
        self.num_of_moves_to_get_to_state = num_of_moves_to_get_to_state
        self.depth = depth

    def __eq__(self, other):
        return other.actual_game.game_board == self.actual_game.game_board

    def __lt__(self, other):
        return self.priority < other.priority

    # def __hash__(self):
    #     return hash(self.actual_game.game_board_as_string)

class FromTo(Enum):
    INIT_TO_SOL = 1
    SOL_TO_INIT = 2


class doubleAstar:
    def __init__(self, initial_board: Board, sol_board: Board, timer, game_number):
        self.sol_min_state: GameState = None
        self.init_min_state: GameState = None
        self.min_depth = sys.maxsize
        self.max_depth = -sys.maxsize
        self.total_heurstic = 0
        self.start_time = time.time()
        self.initial_board = initial_board
        self.sol_board = sol_board
        self.timer = timer
        self.game_number = game_number
        self.sol_open = []
        self.sol_closed = {}
        self.init_open = []
        self.init_closed = {}
        self.init_red_car_info = initial_board.cars_information.get('X')
        self.copy_init_red_car_info = initial_board.cars_information.get('X')
        self.init_curr_state = self.translate_board_to_state(initial_board, self.init_red_car_info)
        self.init_priority = self.init_curr_state.priority
        self.init_closed[self.initial_board.game_board_as_string] = self.init_curr_state
        self.hash_for_init_open = {}
        list = self.expand(initial_board, self.init_curr_state)
        for state in list:
            self.hash_for_init_open[state.actual_game.game_board_as_string] = state
            heappush(self.init_open, state)
        self.hash_for_sol_open = {}
        self.sol_red_car_info = sol_board.cars_information.get('X')
        self.sol_curr_state = self.translate_board_to_state(sol_board, self.sol_red_car_info, True, self.copy_init_red_car_info)
        self.sol_curr_state.priority *= -1
        self.sol_closed[self.sol_board.game_board_as_string] = self.sol_curr_state
        list = self.expand(sol_board, self.sol_curr_state, True,  self.copy_init_red_car_info)
        for state in list:
            self.hash_for_sol_open[state.actual_game.game_board_as_string] = state
            heappush(self.sol_open, state)
        self.algorithm()

    def translate_board_to_state(self, actual_game: Board, red_car_info: Car, is_sol=False, red_init_info=None):
        if is_sol:
                return GameState(self.get_sol_priority(red_car_info.end_col, red_init_info), None, None, None, None, actual_game, 0, 0)
        return GameState(self.get_priority(self.copy_init_red_car_info, red_car_info.end_col, 1), None, None, None, None, actual_game, 0, 0)

    # wrapper function, do not call unless in evaluate_fn
    @staticmethod
    def evaluate_initial_fn(game_board, red_car_end_col):
        counter = 0
        for i in range(red_car_end_col + 1, 6):
            if game_board[2][i] != '.':
                counter += 1
        return counter

    def expand(self, which_board: Board, which_state: GameState, is_sol=False, init_red_car_info=None):
        state_list = []
        for car_name in which_board.cars_information.keys():
            current_car_info: Car = which_board.cars_information.get(car_name)
            state_list_per_car = self.generate_state_for_all_possible_moves(car_name, current_car_info, which_board, which_state, is_sol, init_red_car_info)
            state_list += state_list_per_car
        for state in state_list:
            self.total_heurstic += state.priority
        return state_list

    def generate_state_for_all_possible_moves(self, car_name, car_information: Car, which_board: Board, which_state: GameState, is_sol, init_red_car_info):
        red_car_end_col = which_board.cars_information.get("X").end_col
        if car_information.direction == Direction.ROW:
            return self.get_game_states_in_row(car_name, red_car_end_col, which_board, which_state, is_sol, init_red_car_info)
        elif car_information.direction == Direction.COL:
            return self.get_game_states_in_col(car_name, car_information, red_car_end_col, which_board, which_state, is_sol, init_red_car_info)
        raise Exception("Incorrect Direction in generate_state_for_all_possible_moves")

    def get_game_states_in_row(self, car_name, red_car_end_col, which_board: Board, which_state: GameState, is_sol, init_red_car_info):
        list_states = []
        for i in range(4):
            move = 4 - i
            if which_board.is_legal_move(car_name, move):
                board_copy = deepcopy(which_board)
                board_copy.do_the_move(car_name, move)
                game_state = GameState(1 + which_state.priority, car_name, move, MoveDirection.RIGHT, which_state, board_copy, which_state.num_of_moves_to_get_to_state + 1, which_state.depth+1)
                if is_sol:
                    game_state.priority = self.get_sol_priority(red_car_end_col, init_red_car_info)
                list_states.append(game_state)
        for i in range(-4, 0):
            if which_board.is_legal_move(car_name, i):
                board_copy = deepcopy(which_board)
                board_copy.do_the_move(car_name, i)
                game_state = GameState(1 + which_state.priority, car_name, abs(i), MoveDirection.LEFT, which_state, board_copy, which_state.num_of_moves_to_get_to_state + 1, which_state.depth+1)
                if is_sol:
                    game_state.priority = self.get_sol_priority(red_car_end_col, init_red_car_info)
                list_states.append(game_state)
        return list_states

    def get_game_states_in_col(self, car_name, car_information, red_car_end_col, which_board: Board, which_state: GameState, is_sol, init_red_car_info):
        list_states = []
        for i in range(4):
            if which_board.is_legal_move(car_name, i):
                priority = self.get_priority(car_information, red_car_end_col, i)
                board_copy = deepcopy(which_board)
                board_copy.do_the_move(car_name, i)
                game_state = GameState(1 + priority + which_state.priority, car_name, i, MoveDirection.DOWN, which_state, board_copy, which_state.num_of_moves_to_get_to_state + 1, which_state.depth+1)
                if is_sol:
                    game_state.priority = self.get_sol_priority(red_car_end_col, init_red_car_info)
                list_states.append(game_state)
        for i in range(-4, 0):
            if which_board.is_legal_move(car_name, i):
                priority = self.get_priority(car_information, red_car_end_col, i)
                board_copy = deepcopy(which_board)
                board_copy.do_the_move(car_name, i)
                game_state = GameState(1 + priority + which_state.priority, car_name, abs(i), MoveDirection.UP, which_state, board_copy, which_state.num_of_moves_to_get_to_state + 1, which_state.depth+1)
                if is_sol:
                    game_state.priority = self.get_sol_priority(red_car_end_col, init_red_car_info)
                list_states.append(game_state)
        return list_states

    def get_sol_priority(self, red_car_end_col, init_red_car_info):
        # return abs(red_car_end_col - init_red_car_info.end_col) / 6
        return abs(self.sol_board.heuristic_function8()-self.init_priority)

    def get_priority(self, car_information: Car, red_car_end_col, steps):
        # if car_information.direction == Direction.ROW:
        #     return 0
        # if red_car_end_col > car_information.start_col:
        #     return 0
        # final_start_row = car_information.start_row + steps
        # final_end_row = car_information.end_row + steps
        # car_was_near_line_3 = 2 in range(car_information.start_row, car_information.end_row + 1)
        # car_will_be_near_line_3 = 2 in range(final_start_row, final_end_row + 1)
        # if car_was_near_line_3 and not car_will_be_near_line_3:
        #     return -1
        # elif not car_was_near_line_3 and car_will_be_near_line_3:
        #     return 1
        # return 0
        # return 6 - red_car_end_col / 6
        return self.initial_board.heuristic_function8()


    def algorithm(self):
        flag_to_get_out = False
        steps_so_far = 0
        while self.init_open or self.sol_open:
            if time.time() - self.start_time >= self.timer:
                f = open(F_OUTPUT_DOUBLE_A_STAR_FILE, "a")
                f.write("\nGame number{}, FAILED \n".format(self.game_number))
                break
            # HERE WE CHECK THE INIT BOARD AND STATES IF IT HAS BEEN REACHED AND AFTER THAT WE WILL CHECK THE OTHER CASE :
            init_popped_state: GameState = heappop(self.init_open)
            list_for_min_states = [init_popped_state]
            if self.does_it_exist_in_other_mapping(FromTo.INIT_TO_SOL, init_popped_state, init_popped_state.actual_game):
                self.found_a_solution()
            while 1:
                # if heap becomes empty, stop looping:
                if not self.init_open:
                    break
                curr_min_priority_in_heap = self.init_open[0].priority
                if curr_min_priority_in_heap != init_popped_state.priority:
                    break
                another_min_state = heappop(self.init_open)
                if self.does_it_exist_in_other_mapping(FromTo.INIT_TO_SOL, another_min_state, another_min_state.actual_game):
                    self.found_a_solution()
                list_for_min_states.append(another_min_state)
            index = random.randint(0, len(list_for_min_states) - 1)
            init_popped_state = list_for_min_states[index]
            # here we didn't got our goal yet so we deal only with a one state so we push the rest
            for i in range(0, len(list_for_min_states)):
                if i == index:
                    continue
                heappush(self.init_open, list_for_min_states[i])

            self.initial_board = deepcopy(init_popped_state.prev_state.actual_game)  # TODO: Do we need deep copy?

            # add the min state to closed hash
            self.initial_board.move_car(init_popped_state.car_name, init_popped_state.direction, init_popped_state.steps)
            self.init_closed[self.initial_board.game_board_as_string] = init_popped_state
            self.init_curr_state = init_popped_state

            # expand the min gameState
            steps_so_far += 1
            list_for_expand = self.expand(self.initial_board, self.init_curr_state)
            for state in list_for_expand:
                # index_for_state_in_open = self.does_it_exist_in_open(state, self.init_open)
                state_in_open: GameState = self.hash_for_init_open.get(state.actual_game.game_board_as_string)
                exists_in_open = state_in_open is not None
                # copy_of_board: Board = deepcopy(self.initial_board)
                self.initial_board.move_car(state.car_name, state.direction, state.steps)
                state_in_closed: GameState = self.init_closed.get(self.initial_board.game_board_as_string)
                exists_in_closed: bool = state_in_closed is not None
                if not exists_in_closed and not exists_in_open:
                    state.prev_state = init_popped_state
                    self.hash_for_init_open[state.actual_game.game_board_as_string] = state
                    heappush(self.init_open, state)
                elif exists_in_closed:
                    if state_in_closed.priority > state.priority:
                        self.init_closed.pop(self.initial_board.game_board_as_string)
                        self.hash_for_init_open[state.actual_game.game_board_as_string] = state
                        heappush(self.init_open, state)
                else:
                    if state_in_open.priority > state.priority:
                        self.init_open.remove(state_in_open)
                        self.hash_for_init_open[state.actual_game.game_board_as_string] = state
                        heappush(self.init_open, state)
                if self.does_it_exist_in_other_mapping(FromTo.INIT_TO_SOL, state, self.initial_board):
                    self.found_a_solution()
                    flag_to_get_out = True
                    break
                self.initial_board.move_car(state.car_name, self.get_opp_side(state.direction), state.steps)
            if flag_to_get_out:
                break
            # OTHER CASE:
            # ==============================================================
            # ==============================================================
            # ==============================================================
            # ==============================================================
            # ==============================================================
            sol_popped_state: GameState = heappop(self.sol_open)

            list_for_min_states = [sol_popped_state]
            if self.does_it_exist_in_other_mapping(FromTo.SOL_TO_INIT, sol_popped_state, sol_popped_state.actual_game):
                self.found_a_solution()
            while 1:
                # if heap becomes empty, stop looping:
                if not self.sol_open:
                    break
                curr_min_priority_in_heap = self.sol_open[0].priority
                if curr_min_priority_in_heap != sol_popped_state.priority:
                    break
                another_min_state = heappop(self.sol_open)
                if self.does_it_exist_in_other_mapping(FromTo.SOL_TO_INIT, another_min_state, another_min_state.actual_game):
                    self.found_a_solution()
                list_for_min_states.append(another_min_state)
            index = random.randint(0, len(list_for_min_states) - 1)
            sol_popped_state = list_for_min_states[index]
            # here we didn't got our goal yet so we deal only with a one state so we push the rest
            for i in range(0, len(list_for_min_states)):
                if i == index:
                    continue
                heappush(self.sol_open, list_for_min_states[i])

            self.sol_board = deepcopy(sol_popped_state.prev_state.actual_game)  # TODO: Do we need deep copy?

            # add the min state to closed hash
            self.sol_board.move_car(sol_popped_state.car_name, sol_popped_state.direction, sol_popped_state.steps)
            self.sol_closed[self.sol_board.game_board_as_string] = sol_popped_state
            self.sol_curr_state = sol_popped_state

            # expand the min gameState
            steps_so_far += 1
            list_for_expand = self.expand(self.sol_board, self.sol_curr_state, True, self.copy_init_red_car_info)
            for state in list_for_expand:
                # index_for_state_in_open = self.does_it_exist_in_open(state, self.sol_open)
                state_in_open: GameState = self.hash_for_sol_open.get(state.actual_game.game_board_as_string)
                exists_in_open = state_in_open is not None
                # copy_of_board: Board = deepcopy(self.sol_board)
                self.sol_board.move_car(state.car_name, state.direction, state.steps)
                state_in_closed: GameState = self.sol_closed.get(self.sol_board.game_board_as_string)
                exists_in_closed: bool = state_in_closed is not None
                if not exists_in_closed and not exists_in_open:
                    state.prev_state = sol_popped_state
                    self.hash_for_sol_open[state.actual_game.game_board_as_string] = state
                    heappush(self.sol_open, state)
                elif exists_in_closed:
                    if state_in_closed.priority > state.priority:
                        self.sol_closed.pop(self.sol_board.game_board_as_string)
                        self.hash_for_sol_open[state.actual_game.game_board_as_string] = state
                        heappush(self.sol_open, state)
                else:
                    if state_in_open.priority > state.priority:
                        self.sol_open.remove(state_in_open)
                        self.hash_for_sol_open[state.actual_game.game_board_as_string] = state
                        heappush(self.sol_open, state)
                if self.does_it_exist_in_other_mapping(FromTo.SOL_TO_INIT, state, self.sol_board):
                    self.found_a_solution()
                self.sol_board.move_car(state.car_name, self.get_opp_side(state.direction), state.steps)
        self.print_steps(self.sol_min_state, self.init_min_state)
        # print('\n')

    def print_steps(self, sol_min_state: GameState, init_min_state: GameState):
        f = open(F_OUTPUT_DOUBLE_A_STAR_FILE, "a")
        f.write('Game No\'{}, took {} sec, {} depth\n'.format(self.game_number, time.time() - self.start_time, self.min_depth))
        sol_list_of_steps = []
        while sol_min_state.prev_state is not None:
            sol_min_state.direction = self.get_opp_side(sol_min_state.direction)
            sol_list_of_steps.append(self.get_step_in_str(sol_min_state))
            sol_min_state = sol_min_state.prev_state
        steps_to_get_red_out = 6 - sol_min_state.actual_game.red_car_info.end_col + 1
        sol_list_of_steps.append("XR{}".format(steps_to_get_red_out))
        # list_of_steps.reverse()
        list_of_steps = []
        while init_min_state.prev_state is not None:
            list_of_steps.append(self.get_step_in_str(init_min_state))
            init_min_state = init_min_state.prev_state
        list_of_steps.reverse()
        list_of_steps += sol_list_of_steps
        # print(list_of_steps)
        j = 0
        for i in range(len(list_of_steps)):
            if j == 10:
                j = 0
                f.write('\n')
                f.write('                     ')
            j += 1
            f.write("{} ".format(list_of_steps[i]))
        f.write('.\n              \n')
        f.write('Searched nodes = {} !\n'.format(len(self.sol_open) + len(self.sol_closed) + len(self.init_open) + len(self.init_closed)))
        f.write('Max depth {} !\n'.format(self.max_depth))
        f.write('AVG {} !\n\n'.format(self.total_heurstic/(len(self.sol_open) + len(self.sol_closed) + len(self.init_open) + len(self.init_closed))))


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

    @staticmethod
    def does_it_exist_in_open(state: GameState, list):
        open_length: int = len(list)
        for i in range(open_length):
            if state == list[i]:
                return i
        return -1

    def does_it_exist_in_other_mapping(self, from_to, state, copy_of_board: Board):
        if from_to == FromTo.INIT_TO_SOL:
            state_in_sol_closed = self.sol_closed.get(copy_of_board.game_board_as_string)
            exists_in_sol_closed: bool = state_in_sol_closed is not None
            state_in_sol_open = self.hash_for_sol_open.get(copy_of_board.game_board_as_string)
            exists_in_sol_open: bool = state_in_sol_open is not None
            if exists_in_sol_closed or exists_in_sol_open:
                if exists_in_sol_open:
                    total_depth = state.depth + state_in_sol_open.depth
                else:
                    total_depth = state.depth + state_in_sol_closed.depth
                if total_depth > self.max_depth:
                    self.max_depth = total_depth
                if total_depth < self.min_depth:
                    self.min_depth = total_depth
                    self.init_min_state = state
                    if exists_in_sol_open:
                        self.sol_min_state = state_in_sol_open
                    else:
                        self.sol_min_state = state_in_sol_closed
                return True
            else:
                return False
        else:
            state_in_init_closed = self.init_closed.get(copy_of_board.game_board_as_string)
            exists_in_init_closed: bool = state_in_init_closed is not None
            state_in_init_open = self.hash_for_init_open.get(copy_of_board.game_board_as_string)
            exists_in_init_open: bool = state_in_init_open is not None
            if exists_in_init_closed or exists_in_init_open:
                if exists_in_init_open:
                    total_depth = state.depth + state_in_init_open.depth
                else:
                    total_depth = state.depth + state_in_init_closed.depth
                if total_depth < self.min_depth:
                    self.min_depth = total_depth
                    if exists_in_init_closed:
                        self.init_min_state = state_in_init_closed
                    else:
                        self.init_min_state = state_in_init_open
                    self.sol_min_state = state
                return True
            else:
                return False

    def found_a_solution(self):
        # print('Game No\'{}, took{}sec\n'.format(self.game_number, time.time()-self.start_time))
        pass

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
