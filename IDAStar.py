import time

from board import Board, Car, Direction, MoveDirection
from utils import TODO, UNDEFINED_F_VALUE, INFINITY, F_OUTPUT_IDA_STAR_FILE


class IDAStarGameState:

    def __init__(self, car_name, steps, direction, actual_game: Board, num_of_moves_to_get_to_state,
                 heuristic_function):
        self.f_value = UNDEFINED_F_VALUE
        self.car_name = car_name
        self.steps: int = steps
        self.direction: MoveDirection = direction
        self.actual_game = actual_game.copy_me()
        if steps != 0:
            self.actual_game.move_car_faithfully(car_name, direction, steps)
        self.num_of_moves_to_get_to_state: int = num_of_moves_to_get_to_state
        self.heuristic_function = heuristic_function
        self.evaluate_f_value()

    def __str__(self):
        root = ""
        if self.steps == 0:
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
        elif self.heuristic_function == 5:
            self.f_value = self.heuristic_function5()
        elif self.heuristic_function == 6:
            self.f_value = self.heuristic_function6()
        elif self.heuristic_function == 7:
            self.f_value = self.heuristic_function7()
        elif self.heuristic_function == 8:
            self.f_value = self.heuristic_function8()
        elif self.heuristic_function == 9:
            self.f_value = self.heuristic_function9()
        elif self.heuristic_function == 10:
            self.f_value = self.heuristic_function10()
        elif self.heuristic_function == 11:
            self.f_value = self.heuristic_function11()
        elif self.heuristic_function == 12:
            self.f_value = self.heuristic_function12()
        else:
            TODO("Unexpected heuristic value in class \"{}\", was: {}".format(type(self).__name__,
                                                                              self.heuristic_function))
        self.f_value += self.num_of_moves_to_get_to_state

    def heuristic_function1(self):
        return self.actual_game.heuristic_function1()

    def heuristic_function2(self):
        return self.actual_game.num_of_cars_in_third_row()

    def heuristic_function4(self):
        return self.actual_game.num_of_cars_blocked_infront_of_red()

    def heuristic_function5(self):
        return self.actual_game.heuristic_function5()

    def heuristic_function6(self):
        return self.actual_game.heuristic_function6_haha()

    def heuristic_function7(self):
        return pow(2, self.actual_game.num_of_cars_in_third_row())

    def heuristic_function8(self):
        return self.actual_game.heuristic_function8()

    def heuristic_function9(self):
        return self.heuristic_function7() + self.actual_game.heuristic_function8()

    # wrapper function, do not call unless in heuristic_one_mn_shan_allah_em7a_elfonktsya
    @staticmethod
    def evaluate_initial_fn(game_board, red_car_end_col):
        counter = 0
        for i in range(red_car_end_col + 1, 6):
            if game_board[2][i] != '.':
                counter += 1
        return counter

    def is_head(self):
        return self.steps == 0

    @staticmethod
    def get_step_in_str(node):
        if node.is_head():
            pass
        direction_map = {
            MoveDirection.UP: "U",
            MoveDirection.DOWN: "D",
            MoveDirection.LEFT: "L",
            MoveDirection.RIGHT: "R"
        }
        return "{}{}{}".format(node.car_name, direction_map.get(node.direction), node.steps)

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

        state_list.sort()
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
            move = 4 - i
            if self.actual_game.is_legal_move(car_name, move):
                list_states.append(
                    IDAStarGameState(car_name, move, MoveDirection.RIGHT, self.actual_game,
                                     self.num_of_moves_to_get_to_state + 1, heuristic_function)
                )
        for i in range(-4, 0):
            if self.actual_game.is_legal_move(car_name, i):
                list_states.append(
                    IDAStarGameState(car_name, -i, MoveDirection.LEFT, self.actual_game,
                                     self.num_of_moves_to_get_to_state + 1, heuristic_function)
                )

        return list_states

    def get_game_states_in_col(self, car_name, heuristic_function):
        list_states = []
        for i in range(4):
            if self.actual_game.is_legal_move(car_name, i):
                list_states.append(
                    IDAStarGameState(car_name, i, MoveDirection.DOWN, self.actual_game,
                                     self.num_of_moves_to_get_to_state + 1, heuristic_function)
                )
        for i in range(-4, 0):
            if self.actual_game.is_legal_move(car_name, i):
                list_states.append(
                    IDAStarGameState(car_name, -i, MoveDirection.UP, self.actual_game,
                                     self.num_of_moves_to_get_to_state + 1, heuristic_function)
                )

        return list_states


class IDAStar:

    @staticmethod
    def print_steps(game_index, start_time, path):
        list_of_steps = []
        while path:
            node: IDAStarGameState = path.pop()
            list_of_steps.append(node.get_step_in_str(node))
        list_of_steps.reverse()
        # print(list_of_steps)
        # self.print_board_after_doing_all_steps(list_of_steps)
        f = open(F_OUTPUT_IDA_STAR_FILE, "a")
        f.write("\nGame number{}, Steps: ".format(game_index))
        j = 0
        for i in range(1, len(list_of_steps)):
            if j == 10:
                j = 0
                f.write('\n')
                f.write('                     ')
            j += 1
            f.write("{} ".format(list_of_steps[i]))
        f.write('.\n              ')
        f.write("total time{}\n".format(time.time() - start_time))
        f.close()
        pass

    def __init__(self, game_board: Board, game_index, heuristic_function, allocated_time):
        # time and output calculations
        start_time = time.time()

        # actual algorithms
        self.root = None
        self.visited_nodes = {}
        self.heuristic_function = heuristic_function
        path, bound = self.algorithm(game_board, start_time, allocated_time)
        if path is not None:
            self.print_steps(game_index, start_time, path)
        else:
            f = open(F_OUTPUT_IDA_STAR_FILE, "a")
            f.write("\nGame number{}, FAILED on allocated time: {}".format(game_index, allocated_time))

    def algorithm(self, game_board: Board, start_time, allocated_time):
        path = []
        hashed_path = {}
        self.visited_nodes = {}
        self.root = IDAStarGameState(None, 0, None, game_board, 0, self.heuristic_function)
        current_bound = self.root.f_value
        while True:
            passed_time = time.time() - start_time
            if passed_time > allocated_time:
                return None, None
            path.clear()
            hashed_path.clear()
            self.visited_nodes.clear()
            path = [self.root]
            hashed_path = {self.root.get_hash(): self.root}
            hashed_path, path, suspected_bound, is_found = self.search(path, current_bound, hashed_path)
            if is_found:
                return path, current_bound
            if suspected_bound >= INFINITY:
                return None, None
            current_bound = suspected_bound

    def search(self, path, current_bound, hashed_path):
        node: IDAStarGameState = path[-1]  # last element
        self.visited_nodes[node.get_hash()] = node
        f = node.f_value
        if f > current_bound:
            return hashed_path, path, f, False
        if node.is_win_state():
            return hashed_path, path, f, True
        minimum = INFINITY
        children = node.expand(self.heuristic_function)
        for child in children:
            if not self.ever_seen_this_node(child):
                path.append(child)
                hashed_path[child.get_hash()] = child
                hashed_path, path, suspected_bound, is_found = self.search(path, current_bound, hashed_path)
                if is_found:
                    return hashed_path, path, f, True
                minimum = min(minimum, suspected_bound)
                path.pop()
                hashed_path.pop(child.get_hash())
        return hashed_path, path, minimum, False

    def ever_seen_this_node(self, node: IDAStarGameState):
        return self.visited_nodes.get(node.get_hash()) is not None
