import heapq

from board import *


class GameState:

    def __init__(self, priority, car_name, steps, direction):
        self.priority = priority
        self.car_name = car_name
        self.steps = steps
        self.direction = direction


class AStarAlgorithm:
    # unexpanded nodes:
    closed = []
    # expanded nodes:
    open = []

    # tuple of board & fn
    current_state: GameState = None

    # the Board Data Structure:
    actual_game: Board = None

    def __init__(self, actual_game, red_car_info):
        self.closed = []
        self.open = []
        # also initial state:
        self.current_state = self.translate_board_to_state(actual_game.game_board, 0, red_car_info)
        self.actual_game = actual_game

    def translate_board_to_state(self, board, steps, red_car_info: Car):
        # TODO: Notice! Missing Parameter....
        return GameState(self.evaluate_fn(board, steps, red_car_info.end_col), board)

    # wrapper function, do not call unless in evaluate_fn
    @staticmethod
    def evaluate_hn(board, red_car_end_col):
        # TODO: Should add other hn
        counter = 0
        for i in range(red_car_end_col + 1, 6):
            if board[2][i] != '.':
                counter += 1
        return counter

    def evaluate_fn(self, board, steps_so_far, red_car_end_col):
        hn = self.evaluate_hn(board, red_car_end_col)
        gn = steps_so_far
        return hn + gn

    # expands the current state
    def expand(self, steps_so_far):
        red_car_end_col = self.actual_game.cars_information.get("X").end_col
        state_list = self.generate_all_states_from_current_state(red_car_end_col)
        return self.evaluate_fn_for_all_states(state_list, steps_so_far)

    def generate_all_states_from_current_state(self, red_car_end_col):
        state_list = []
        for car_name in self.actual_game.cars_information.keys():
            state_list_per_car = self.generate_state_for_all_possible_moves(car_name, self.actual_game.cars_information.get(car_name), red_car_end_col)
            state_list += state_list_per_car

        return state_list

    def generate_state_for_all_possible_moves(self, car_name , car_information: Car, red_car_end_col):
        if car_information.direction == Direction.ROW:
            return self.get_game_states_in_row(car_name, car_information, red_car_end_col)
        elif car_information.direction == Direction.COL:
            return self.get_game_states_in_col(car_name, car_information, red_car_end_col)
        raise Exception("Incorrect Direction in generate_state_for_all_possible_moves")

    def get_game_states_in_row(self, car_name, car_information, red_car_end_col):
        list_states = []
        for i in range(4):
            if self.actual_game.is_legal_move(car_name, i):
                list_states.append(GameState(0, car_name, i, Direction.ROW))
        for i in range(-4 , -1):
            if self.actual_game.is_legal_move(car_name, i):
                list_states.append(GameState(0, car_name, i, Direction.ROW))
        return list_states

    def get_game_states_in_col(self, car_name, car_information, red_car_end_col):
        list_states = []
        for i in range(4):
            if self.actual_game.is_legal_move(car_name, i):
                priority = self.get_priority(car_information, red_car_end_col, i)
                list_states.append(GameState(priority, car_name, i, Direction.COL))
        for i in range(-4, -1):
            if self.actual_game.is_legal_move(car_name, i):
                priority = self.get_priority(car_information, red_car_end_col, i)
                list_states.append(GameState(priority, car_name, i, Direction.COL))
        return list_states

    @staticmethod
    def get_priority(car_information: Car, red_car_end_col, i):
        if red_car_end_col > car_information.start_col:
            return 0
        final_start_row = car_information.start_row + i
        final_end_row = car_information.end_row + i
        car_was_near_line_3 = 2 in range(car_information.start_row, car_information.end_row)
        car_will_be_near_line_3 = 2 in range(final_start_row, final_end_row)
        if car_was_near_line_3 and not car_will_be_near_line_3:
            return -1
        elif not car_was_near_line_3 and car_will_be_near_line_3:
            return 1
        return 0

    def evaluate_fn_for_all_states(self, state_list, steps_so_far):
        for state in state_list:
            new_expected_value = state.priority + steps_so_far
            if state.priority >= new_expected_value:
                state.priority = new_expected_value
        return state_list
