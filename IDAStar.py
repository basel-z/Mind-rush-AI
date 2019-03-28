import time
from copy import deepcopy

from board import Board
from board import Car
from board import Direction
from board import MoveDirection
from utils import TODO, UNDEFINED_F_VALUE, INFINITY


class IDAStarGameState:

    def __init__(self, car_name, steps, direction, prev_state, actual_game, num_of_moves_to_get_to_state,
                 heuristic_function):
        self.f_value = UNDEFINED_F_VALUE
        self.car_name = car_name
        self.steps: int = steps
        self.direction: MoveDirection = direction
        self.actual_game: Board = actual_game
        self.num_of_moves_to_get_to_state: int = num_of_moves_to_get_to_state
        self.prev_state = prev_state
        self.heuristic_function = heuristic_function
        self.evaluate_f_value()

    def __str__(self):
        root = ""
        if self.prev_state is None:
            root = "[root] "
        return "{}({},{}): {} {} {}".format(root, self.f_value, self.num_of_moves_to_get_to_state, self.car_name,
                                            self.direction, self.steps)

    def __eq__(self, other):
        return other.actual_game.game_board_as_string == self.actual_game.game_board_as_string

    def __lt__(self, other):
        return self.f_value < other.f_value

    def evaluate_f_value(self):
        if self.heuristic_function == 1:
            self.f_value = self.heuristic_function1()
        elif self.heuristic_function == 2:
            self.f_value = self.heuristic_function2()
        elif self.heuristic_function == 4:
            self.f_value = self.heuristic_function4()
        else:
            TODO("Unexpected heuristic value in class \"{}\", was: {}".format(type(self).__name__,
                                                                              self.heuristic_function))

    def heuristic_function2(self):
        return TODO("Heuristic function 2 not implemented.")

    def heuristic_function4(self):
        return TODO("Heuristic function 4 not implemented.")

    def heuristic_function1(self):
        if self.prev_state is None:
            return self.evaluate_initial_fn(self.actual_game.game_board,
                                            self.actual_game.cars_information.get('X').end_col)
        value = self.get_priority(self.actual_game.cars_information.get(self.car_name),
                                  self.actual_game.red_car_info.end_col, self.steps)
        prev_f_value = self.get_prev_f_value()
        return value + prev_f_value + 1

    def get_prev_f_value(self):
        if self.prev_state is None:
            return 0
        return self.prev_state.f_value

    # wrapper function, do not call unless in heuristic_one_mn_shan_allah_em7a_elfonktsya
    @staticmethod
    def evaluate_initial_fn(game_board, red_car_end_col):
        counter = 0
        for i in range(red_car_end_col + 1, 6):
            if game_board[2][i] != '.':
                counter += 1
        return counter

    def is_head(self):
        return self.prev_state is None

    def print_steps(self, game_index, start_time):
        list_of_steps = []
        node = self
        while not node.is_head():
            list_of_steps.append(self.get_step_in_str(node))
            node = node.prev_state
        list_of_steps.reverse()
        # print(list_of_steps)
        # self.print_board_after_doing_all_steps(list_of_steps)
        f = open("output.txt", "a")
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
        f.write("total time{}\n".format(time.time() - start_time))
        f.close()

    @staticmethod
    def get_step_in_str(prev_state):
        if prev_state.direction == MoveDirection.UP:
            return "{}U{}".format(prev_state.car_name, prev_state.steps)
        if prev_state.direction == MoveDirection.DOWN:
            return "{}D{}".format(prev_state.car_name, prev_state.steps)
        if prev_state.direction == MoveDirection.LEFT:
            return "{}L{}".format(prev_state.car_name, prev_state.steps)
        if prev_state.direction == MoveDirection.RIGHT:
            return "{}R{}".format(prev_state.car_name, prev_state.steps)

    def print_board_after_doing_all_steps(self, list_of_steps):
        tmp_board: Board = self.actual_game
        for move in list_of_steps:
            move_side = MoveDirection.UP
            _move = move[1]
            if _move == 'D':
                move_side = MoveDirection.DOWN
            elif _move == 'L':
                move_side = MoveDirection.LEFT
            elif _move == 'R':
                move_side = MoveDirection.RIGHT
            tmp_board.move_car(move[0], move_side, ord(move[2]) - ord('0'))
        self.print_game_comfortably(tmp_board)

    @staticmethod
    def print_game_comfortably(board: Board):
        for line in board.game_board:
            print(" ".join(line))
        print()

    def get_hash(self):
        return self.actual_game.game_board_as_string

    def is_win_state(self):
        red_car_end_col = self.actual_game.cars_information.get('X').end_col
        range_index = 6 - red_car_end_col
        for i in range(1, range_index):
            if self.actual_game.game_board[2][red_car_end_col + i] != '.':
                return False
        return True

    # expands the current state
    def expand(self, heuristic_function):
        state_list = []
        for car_name in self.actual_game.cars_information.keys():
            current_car_info: Car = self.actual_game.cars_information.get(car_name)
            state_list_per_car = self.generate_state_for_all_possible_moves(car_name, current_car_info,
                                                                            heuristic_function)
            state_list += state_list_per_car

        return state_list

    def generate_state_for_all_possible_moves(self, car_name, car_information: Car, heuristic_function):
        if car_information.direction == Direction.ROW:
            return self.get_game_states_in_row(car_name, heuristic_function)
        elif car_information.direction == Direction.COL:
            return self.get_game_states_in_col(car_name, heuristic_function)
        raise Exception("Incorrect Direction in generate_state_for_all_possible_moves")

    def get_game_states_in_row(self, car_name, heuristic_function):
        list_states = []
        for i in range(4):
            if self.actual_game.is_legal_move(car_name, i):
                board_copy = deepcopy(self.actual_game)
                board_copy.do_the_move(car_name, i)
                list_states.append(
                    # DFSNode(self.depth + 1, GameState(board_copy, car_name, MoveDirection.RIGHT, i), self) TODO: Be extra careful
                    IDAStarGameState(car_name, i, MoveDirection.RIGHT, self, board_copy,
                                     self.num_of_moves_to_get_to_state + 1, heuristic_function)
                )
        for i in range(-4, 0):
            if self.actual_game.is_legal_move(car_name, i):
                board_copy = deepcopy(self.actual_game)
                board_copy.do_the_move(car_name, i)
                list_states.append(
                    # DFSNode(self.depth + 1, GameState(board_copy, car_name, MoveDirection.LEFT, -i), self) TODO: Be extra careful
                    IDAStarGameState(car_name, -i, MoveDirection.LEFT, self, board_copy,
                                     self.num_of_moves_to_get_to_state + 1, heuristic_function)
                )

        return list_states

    def get_game_states_in_col(self, car_name, heuristic_function):
        list_states = []
        for i in range(4):
            if self.actual_game.is_legal_move(car_name, i):
                board_copy = deepcopy(self.actual_game)
                board_copy.do_the_move(car_name, i)
                list_states.append(
                    IDAStarGameState(car_name, i, MoveDirection.DOWN, self, board_copy,
                                     self.num_of_moves_to_get_to_state + 1, heuristic_function)
                )
        for i in range(-4, 0):
            if self.actual_game.is_legal_move(car_name, i):
                board_copy = deepcopy(self.actual_game)
                board_copy.do_the_move(car_name, i)
                list_states.append(
                    IDAStarGameState(car_name, -i, MoveDirection.UP, self, board_copy,
                                     self.num_of_moves_to_get_to_state + 1, heuristic_function)
                )

        return list_states

    def get_priority(self, car_information: Car, red_car_end_col, steps):
        if self.direction in [MoveDirection.LEFT, MoveDirection.RIGHT]:
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


class IDAStar:

    def __init__(self, game_board: Board, game_index, heuristic_function, allocated_time):
        # time and output calculations
        start_time = time.time()

        # actual algorithms
        self.root = None
        self.visited_nodes = {}
        self.heuristic_function = heuristic_function
        path, bound = self.algorithm(game_board)
        if path is not None:
            v: IDAStarGameState = path.pop()
            v.print_steps(game_index, start_time)

    def algorithm(self, game_board: Board):
        path = []
        hashed_path = {}
        self.visited_nodes = {}
        self.root = IDAStarGameState(None, 0, None, None, game_board, 0, self.heuristic_function)
        current_bound = self.root.f_value
        while True:
            path.clear()
            hashed_path.clear()
            self.visited_nodes.clear()
            path = [self.root]
            hashed_path = {self.root.get_hash(): self.root}
            path, suspected_bound, is_found = self.search(path, current_bound, hashed_path)
            if is_found:
                return path, current_bound
            if suspected_bound == INFINITY:
                return None, None
            current_bound = suspected_bound

    def search(self, path, current_bound, hashed_path):
        node: IDAStarGameState = path[-1]  # last element
        self.visited_nodes[node.get_hash()] = node
        f = node.f_value
        if f > current_bound:
            return path, f, False
        if node.is_win_state():
            return path, f, True
        minimum = INFINITY
        children = node.expand(self.heuristic_function)
        for child in children:
            if hashed_path.get(child.get_hash()) is None and self.visited_nodes.get(child.get_hash()) is None:
                path.append(child)
                hashed_path[child.get_hash()] = child
                path, suspected_bound, is_found = self.search(path, current_bound, hashed_path)
                if is_found:
                    return path, f, True
                minimum = min(minimum, suspected_bound)
                path.pop()
                hashed_path.pop(child.get_hash())
        return path, minimum, False
