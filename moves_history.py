from heapq import *
from copy import deepcopy
from board import *
from game import print_game_comfortably
import time

class GameState:

    def __init__(self, priority, car_name, steps, direction, prev_state, game_board):
        self.priority = priority
        self.car_name = car_name
        self.steps = steps
        self.direction = direction
        self.game_board = game_board
        self.prev_state = prev_state

    def __eq__(self, other):
        return other.game_board == self.game_board

    def __lt__(self, other):
        return self.priority < other.priority


class AStarAlgorithm:
    def __init__(self, actual_game: Board, red_car_info):
        self.start_time = time.time()
        self.closed = {}
        self.open = []
        # also initial state:
        self.current_state = self.translate_board_to_state(actual_game.game_board, 0, red_car_info, actual_game.game_board_as_string)
        self.actual_game: Board = actual_game
        self.closed[self.actual_game.game_board_as_string] = self.current_state
        list = self.expand(0)
        for state in list:
            heappush(self.open, (state.priority, state))
        assert self.algorthim()

    def translate_board_to_state(self, game_board, steps, red_car_info: Car, game_board_as_string):
        # TODO: Notice! Missing Parameter....
        return GameState(self.evaluate_fn(game_board, steps, red_car_info.end_col), None, None, None, None, game_board_as_string)

    # wrapper function, do not call unless in evaluate_fn
    @staticmethod
    def evaluate_hn(game_board, red_car_end_col):
        # TODO: Should add other hn
        counter = 0
        for i in range(red_car_end_col + 1, 6):
            if game_board[2][i] != '.':
                counter += 1
        return counter

    def evaluate_fn(self, game_board, steps_so_far, red_car_end_col):
        hn = self.evaluate_hn(game_board, red_car_end_col)
        gn = steps_so_far
        return hn + gn

    # expands the current state
    def expand(self, steps_so_far):
        red_car_end_col = self.actual_game.cars_information.get("X").end_col
        return self.generate_all_states_from_current_state(red_car_end_col, steps_so_far)

    def generate_all_states_from_current_state(self, red_car_end_col, steps_so_far):
        state_list = []
        for car_name in self.actual_game.cars_information.keys():
            state_list_per_car = self.generate_state_for_all_possible_moves(car_name, self.actual_game.cars_information.get(car_name), red_car_end_col, steps_so_far)
            state_list += state_list_per_car

        return state_list

    def generate_state_for_all_possible_moves(self, car_name, car_information: Car, red_car_end_col, steps_so_far):
        if car_information.direction == Direction.ROW:
            return self.get_game_states_in_row(car_name, car_information, red_car_end_col, steps_so_far)
        elif car_information.direction == Direction.COL:
            return self.get_game_states_in_col(car_name, car_information, red_car_end_col, steps_so_far)
        raise Exception("Incorrect Direction in generate_state_for_all_possible_moves")

    def get_game_states_in_row(self, car_name, car_information: Car, red_car_end_col, steps_so_far):
        list_states = []
        for i in range(4):
            if self.actual_game.is_legal_move(car_name, i):
                priority = 0  # self.get_priority(car_information, red_car_end_col, i)
                board_copy = deepcopy(self.actual_game)
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(priority + 1 + self.current_state.priority, car_name, i, MoveDirection.RIGHT, self.current_state, board_copy.game_board_as_string))
        for i in range(-4, 0):
            if self.actual_game.is_legal_move(car_name, i):
                priority = 0  # self.get_priority(car_information, red_car_end_col, i)
                board_copy = deepcopy(self.actual_game)
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(priority + 1 + self.current_state.priority, car_name, abs(i), MoveDirection.LEFT, self.current_state, board_copy.game_board_as_string))
        return list_states

    def get_game_states_in_col(self, car_name, car_information, red_car_end_col, steps_so_far):
        list_states = []
        for i in range(4):
            if self.actual_game.is_legal_move(car_name, i):
                priority = self.get_priority(car_information, red_car_end_col, i)
                board_copy = deepcopy(self.actual_game)
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(priority + 1 + self.current_state.priority, car_name, i, MoveDirection.DOWN, self.current_state, board_copy.game_board_as_string))
        for i in range(-4, 0):
            if self.actual_game.is_legal_move(car_name, i):
                priority = self.get_priority(car_information, red_car_end_col, i)
                board_copy = deepcopy(self.actual_game)
                board_copy.do_the_move(car_name, i)
                list_states.append(GameState(priority + 1 + self.current_state.priority, car_name, abs(i), MoveDirection.UP, self.current_state, board_copy.game_board_as_string))
        return list_states

    @staticmethod
    def get_priority(car_information: Car, red_car_end_col, i):
        # TODO: deal with row
        if red_car_end_col > car_information.start_col:
            return 0
        final_start_row = car_information.start_row + i
        final_end_row = car_information.end_row + i
        car_was_near_line_3 = 2 in range(car_information.start_row, car_information.end_row + 1)
        car_will_be_near_line_3 = 2 in range(final_start_row, final_end_row + 1)
        if car_was_near_line_3 and not car_will_be_near_line_3:
            return -1
        elif not car_was_near_line_3 and car_will_be_near_line_3:
            return 1
        return 0

    def algorthim(self):
        # heappush(self.open, (self.current_state.priority, self.current_state))
        steps_so_far = 0
        while self.open:
            curr_min_state: GameState = heappop(self.open)[1]
            list_for_min_states = [curr_min_state]
            copy_of_game_board = deepcopy(self.actual_game)
            copy_of_game_board.move_car(curr_min_state.car_name, curr_min_state.direction, curr_min_state.steps)
            if self.check_winning(copy_of_game_board.game_board):
                self.print_steps(curr_min_state)
                return True

            while 1:
                # if heap becomes empty, stop looping:
                if not self.open:
                    break
                curr_min_priority_in_heap = self.open[0][1].priority
                if curr_min_priority_in_heap != curr_min_state.priority:
                    break
                another_min_state = heappop(self.open)[1]
                copy_of_game_board = deepcopy(self.actual_game)
                copy_of_game_board.move_car(another_min_state.car_name, another_min_state.direction, another_min_state.steps)

                if self.check_winning(copy_of_game_board.game_board):
                    # print(another_min_state.car_name)
                    # print(another_min_state.direction)
                    # print(another_min_state.steps)
                    # if copy_of_game_board.game_board_as_string == 'AADE..O.DEB.O.XXB.OCQQQP.CFGGPHHFIIP':
                    #     print('ahlan')
                    # print("hi: {}".format(copy_of_game_board.game_board_as_string))
                    # print("hi: {}".format(another_min_state.prev_state.game_board))
                    # print("hi: {}".format('AADE..O.DEB.O.XXB.OCQQQP.CFGGPHHFIIP'))
                    # print("bi: {}".format(copy_of_game_board.game_board))
                    self.print_steps(another_min_state)
                    return True
                list_for_min_states.append(another_min_state)

            # here we didn't got our goal yet so we deal only with a one state so we push the rest
            for i in range(1, len(list_for_min_states)):
                heappush(self.open, (list_for_min_states[i].priority, list_for_min_states[i]))


            # switch game board
            self.actual_game = Board(curr_min_state.prev_state.game_board)

            # add the min state to closed hash
            self.actual_game.move_car(curr_min_state.car_name, curr_min_state.direction, curr_min_state.steps)
            self.closed[self.actual_game.game_board_as_string] = curr_min_state
            self.current_state = curr_min_state


            # expand the min gameState
            steps_so_far += 1
            list_for_expand = self.expand(steps_so_far)

            for state in list_for_expand:
                index_for_state_in_open = self.does_it_exist_in_open(state)
                copy_of_board = deepcopy(self.actual_game)
                copy_of_board.move_car(state.car_name, state.direction, state.steps)
                state_in_closed: GameState = self.closed.get(copy_of_board.game_board_as_string)
                exists_in_closed: bool = state_in_closed is not None
                if not exists_in_closed and index_for_state_in_open == -1:
                    state.prev_state = curr_min_state
                    heappush(self.open, (state.priority, state))
                elif exists_in_closed:
                    if state_in_closed.priority > state.priority:
                        self.closed.pop(copy_of_board.game_board_as_string)
                        heappush(self.open, (state.priority, state))
                else:
                    if self.open[index_for_state_in_open][1].priority > state.priority:
                        self.open.remove(self.open[index_for_state_in_open])
                        heappush(self.open, (state.priority, state))
        return False

    def does_it_exist_in_open(self, state: GameState):
        for i in range(len(self.open)):
            if state == self.open[i][1]:
                return i
        return -1

    @staticmethod
    def check_winning(game_board):
        for i in range(6):
            if game_board[2][i] == 'X':
                for j in range(i+2, 6):
                    if game_board[2][j] != '.':
                        return False
                return True
        return True

    def print_steps(self, another_min_state: GameState):
        list_of_steps = []
        while another_min_state.prev_state is not None:
            list_of_steps.append(self.get_step_in_str(another_min_state))
            another_min_state = another_min_state.prev_state
        list_of_steps.reverse()
        self.print_board_after_doing_all_steps(list_of_steps, another_min_state)

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

    def print_board_after_doing_all_steps(self, list_of_steps, another_min_state: GameState):
        tmp_board: Board = Board(another_min_state.game_board)
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
