from board import *
from copy import deepcopy
from heapq import *
import time

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
        return other.actual_game.game_board == self.actual_game.game_board

    def __lt__(self, other):
        return self.priority < other.priority


class FromTo(Enum):
    INIT_TO_SOL = 1
    SOL_TO_INIT = 2


class doubleAstar:
    def __init__(self, initial_board: Board, sol_board: Board, timer, game_number):
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
        self.init_curr_state = self.translate_board_to_state(initial_board, self.init_red_car_info)
        self.init_closed[self.initial_board.game_board_as_string] = self.init_curr_state
        list = self.expand(initial_board, self.init_curr_state)
        for state in list:
            heappush(self.init_open, state)
        self.sol_red_car_info = sol_board.cars_information.get('X')
        self.sol_curr_state = self.translate_board_to_state(sol_board, self.sol_red_car_info)
        self.sol_closed[self.sol_board.game_board_as_string] = self.sol_curr_state
        list = self.expand(sol_board, self.sol_curr_state)
        for state in list:
            heappush(self.sol_open, state)
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

    def expand(self, which_board: Board, which_state: GameState):
        state_list = []
        for car_name in which_board.cars_information.keys():
            current_car_info: Car = which_board.cars_information.get(car_name)
            state_list_per_car = self.generate_state_for_all_possible_moves(car_name, current_car_info, which_board, which_state)
            state_list += state_list_per_car
        return state_list

    def generate_state_for_all_possible_moves(self, car_name, car_information: Car, which_board: Board, which_state: GameState):
        red_car_end_col = which_board.cars_information.get("X").end_col
        if car_information.direction == Direction.ROW:
            return self.get_game_states_in_row(car_name, red_car_end_col, which_board, which_state)
        elif car_information.direction == Direction.COL:
            return self.get_game_states_in_col(car_name, car_information, red_car_end_col, which_board, which_state)
        raise Exception("Incorrect Direction in generate_state_for_all_possible_moves")

    @staticmethod
    def get_game_states_in_row(car_name, red_car_end_col, which_board: Board, which_state: GameState):
        list_states = []
        for i in range(4):
            if which_board.is_legal_move(car_name, i):
                board_copy = deepcopy(which_board)
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(1 + which_state.priority, car_name, i, MoveDirection.RIGHT, which_state, board_copy, which_state.num_of_moves_to_get_to_state + 1))
        for i in range(-4, 0):
            if which_board.is_legal_move(car_name, i):
                board_copy = deepcopy(which_board)
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(1 + which_state.priority, car_name, abs(i), MoveDirection.LEFT, which_state, board_copy, which_state.num_of_moves_to_get_to_state + 1))
        return list_states

    def get_game_states_in_col(self, car_name, car_information, red_car_end_col, which_board: Board, which_state: GameState):
        list_states = []
        for i in range(4):
            if which_board.is_legal_move(car_name, i):
                priority = self.get_priority(car_information, red_car_end_col, i)
                board_copy = deepcopy(which_board)
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(1 + priority + which_state.priority, car_name, i, MoveDirection.DOWN, which_state, board_copy, which_state.num_of_moves_to_get_to_state + 1))
        for i in range(-4, 0):
            if which_board.is_legal_move(car_name, i):
                priority = self.get_priority(car_information, red_car_end_col, i)
                board_copy = deepcopy(which_board)
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(1 + priority + which_state.priority, car_name, abs(i), MoveDirection.UP, which_state, board_copy, which_state.num_of_moves_to_get_to_state + 1))
        return list_states

    @staticmethod
    def get_priority(car_information: Car, red_car_end_col, steps):
        if car_information.direction == Direction.ROW:
            return 0
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
        flag_to_get_out = False
        steps_so_far = 0
        while self.init_open or self.sol_open:
            if time.time() - self.start_time >= self.timer:
                f = open("output.txt", "a")
                f.write("\nGame number{}, FAILED \n".format(self.game_number))
                break
            # HERE WE CHECK THE INIT BOARD AND STATES IF IT HAS BEEN REACHED AND AFTER THAT WE WILL CHECK THE OTHER CASE :
            init_popped_state: GameState = heappop(self.init_open)
            list_for_min_states = [init_popped_state]
            if self.does_it_exist_in_other_mapping(FromTo.INIT_TO_SOL, init_popped_state, init_popped_state.actual_game):
                self.found_a_solution()
                break
            flag = False
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
                    flag = True
                    break
                list_for_min_states.append(another_min_state)
            if flag:
                break

            # here we didn't got our goal yet so we deal only with a one state so we push the rest
            for i in range(1, len(list_for_min_states)):
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
                index_for_state_in_open = self.does_it_exist_in_open(state, self.init_open)
                copy_of_board: Board = deepcopy(self.initial_board)
                copy_of_board.move_car(state.car_name, state.direction, state.steps)
                state_in_closed: GameState = self.init_closed.get(copy_of_board.game_board_as_string)
                exists_in_closed: bool = state_in_closed is not None
                if not exists_in_closed and index_for_state_in_open == -1:
                    state.prev_state = init_popped_state
                    heappush(self.init_open, state)
                elif exists_in_closed:
                    if state_in_closed.priority > state.priority:
                        self.init_closed.pop(copy_of_board.game_board_as_string)
                        heappush(self.init_open, state)
                else:
                    if self.init_open[index_for_state_in_open].priority > state.priority:
                        self.init_open.remove(self.init_open[index_for_state_in_open])
                        heappush(self.init_open, state)
                if self.does_it_exist_in_other_mapping(FromTo.INIT_TO_SOL, state, copy_of_board):
                    self.found_a_solution()
                    flag_to_get_out = True
                    break
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
                break
            flag = False
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
                    flag = True
                    break
                list_for_min_states.append(another_min_state)
            if flag:
                break

            # here we didn't got our goal yet so we deal only with a one state so we push the rest
            for i in range(1, len(list_for_min_states)):
                heappush(self.sol_open, list_for_min_states[i])

            self.sol_board = deepcopy(sol_popped_state.prev_state.actual_game)  # TODO: Do we need deep copy?

            # add the min state to closed hash
            self.sol_board.move_car(sol_popped_state.car_name, sol_popped_state.direction, sol_popped_state.steps)
            self.sol_closed[self.sol_board.game_board_as_string] = sol_popped_state
            self.sol_curr_state = sol_popped_state

            # expand the min gameState
            steps_so_far += 1
            list_for_expand = self.expand(self.sol_board, self.sol_curr_state)
            for state in list_for_expand:
                index_for_state_in_open = self.does_it_exist_in_open(state, self.sol_open)
                copy_of_board: Board = deepcopy(self.sol_board)
                copy_of_board.move_car(state.car_name, state.direction, state.steps)
                state_in_closed: GameState = self.sol_closed.get(copy_of_board.game_board_as_string)
                exists_in_closed: bool = state_in_closed is not None
                if not exists_in_closed and index_for_state_in_open == -1:
                    state.prev_state = sol_popped_state
                    heappush(self.sol_open, state)
                elif exists_in_closed:
                    if state_in_closed.priority > state.priority:
                        self.sol_closed.pop(copy_of_board.game_board_as_string)
                        heappush(self.sol_open, state)
                else:
                    if self.sol_open[index_for_state_in_open].priority > state.priority:
                        self.sol_open.remove(self.sol_open[index_for_state_in_open])
                        heappush(self.sol_open, state)
                if self.does_it_exist_in_other_mapping(FromTo.SOL_TO_INIT, state, copy_of_board):
                    self.found_a_solution()
                    flag_to_get_out = True
                    break
            if flag_to_get_out:
                break
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
            index_in_sol_open = self.does_it_exist_in_open(state, self.sol_open)
            if exists_in_sol_closed or index_in_sol_open != -1:
                return True
            else:
                return False
        else:
            state_in_init_closed = self.init_closed.get(copy_of_board.game_board_as_string)
            exists_in_init_closed: bool = state_in_init_closed is not None
            index_in_init_open = self.does_it_exist_in_open(state, self.init_open)
            if exists_in_init_closed or index_in_init_open != -1:
                return True
            else:
                return False

    def found_a_solution(self):
        print('Game No\'{}, took{}sec\n'.format(self.game_number, time.time()-self.start_time))
