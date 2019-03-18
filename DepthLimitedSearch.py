from board import Board, Car, Direction, MoveDirection
from copy import deepcopy

class GameState:

    def __init__(self, board, car_name, move_direction, steps):
        self.board = board
        self.car_name = car_name
        self.move_direction = move_direction
        self.steps = steps


class DFSNode:

    def is_head(self):
        return self.parent is None

    def print_steps(self):
        list_of_steps = []
        node = self
        while not node.is_head():
            list_of_steps.append(self.get_step_in_str(node.state))
            node = node.parent
        list_of_steps.reverse()
        print(list_of_steps)
        self.print_board_after_doing_all_steps(list_of_steps)

    @staticmethod
    def get_step_in_str(prev_state: GameState):
        if prev_state.move_direction == MoveDirection.UP:
            return "{}U{}".format(prev_state.car_name, prev_state.steps)
        if prev_state.move_direction == MoveDirection.DOWN:
            return "{}D{}".format(prev_state.car_name, prev_state.steps)
        if prev_state.move_direction == MoveDirection.LEFT:
            return "{}L{}".format(prev_state.car_name, prev_state.steps)
        if prev_state.move_direction == MoveDirection.RIGHT:
            return "{}R{}".format(prev_state.car_name, prev_state.steps)

    def print_board_after_doing_all_steps(self, list_of_steps):
        # TODO: Optimize Printing
        tmp_board: Board = self.state.board
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
        self.print_game_comfortably(tmp_board)

    def print_game_comfortably(self, board: Board):
        for line in board.game_board:
            print(" ".join(line))
        print()

    def __init__(self, depth, state, parent):
        self.visited = False
        self.depth: int = depth
        self.state: GameState = state
        self.parent = parent

    def get_hash(self):
        return self.state.board.game_board_as_string

    def is_win(self):
        red_car_end_col = self.state.board.cars_information.get('X').end_col
        range_index = 6 - red_car_end_col
        for i in range(1, range_index):
            if self.state.board.game_board[2][red_car_end_col + i] != '.':
                return False
        return True

    # expands the current state
    def expand(self):
        state_list = []
        for car_name in self.state.board.cars_information.keys():
            current_car_info: Car = self.state.board.cars_information.get(car_name)
            state_list_per_car = self.generate_state_for_all_possible_moves(car_name, current_car_info)
            state_list += state_list_per_car

        return state_list

    def generate_state_for_all_possible_moves(self, car_name, car_information: Car):
        red_car_end_col = self.state.board.cars_information.get("X").end_col
        if car_information.direction == Direction.ROW:
            return self.get_game_states_in_row(car_name, red_car_end_col)
        elif car_information.direction == Direction.COL:
            return self.get_game_states_in_col(car_name, car_information, red_car_end_col)
        raise Exception("Incorrect Direction in generate_state_for_all_possible_moves")

    def get_game_states_in_row(self, car_name, red_car_end_col):
        list_states = []
        for i in range(4):
            if self.state.board.is_legal_move(car_name, i):
                board_copy = deepcopy(self.state.board)
                board_copy.do_the_move(car_name, i)
                list_states.append(DFSNode(self.depth + 1, GameState(board_copy, car_name, MoveDirection.RIGHT, i), self))
        for i in range(-4, 0):
            if self.state.board.is_legal_move(car_name, i):
                board_copy = deepcopy(self.state.board)
                board_copy.do_the_move(car_name, i)
                list_states.append(DFSNode(self.depth + 1, GameState(board_copy, car_name, MoveDirection.LEFT, -i), self))

        return list_states

    def get_game_states_in_col(self, car_name, car_information, red_car_end_col):
        list_states = []
        for i in range(4):
            if self.state.board.is_legal_move(car_name, i):
                board_copy = deepcopy(self.state.board)
                board_copy.do_the_move(car_name, i)
                list_states.append(DFSNode(self.depth + 1, GameState(board_copy, car_name, MoveDirection.DOWN, i), self))
        for i in range(-4, 0):
            if self.state.board.is_legal_move(car_name, i):
                board_copy = deepcopy(self.state.board)
                board_copy.do_the_move(car_name, i)
                list_states.append(DFSNode(self.depth + 1, GameState(board_copy, car_name, MoveDirection.UP, -i), self))

        return list_states


class DepthLimitedSearch:

    def __init__(self, board: Board):
        self.initial_board = board
        self.stack = list()
        self.closed = {}
        win_node: DFSNode = self.dls()
        if win_node is not None:
            win_node.print_steps()

    def dls(self):
        depth_allowed = 0
        while True:
            self.closed.clear()
            winning_state = self.dfs(depth_allowed)
            if winning_state is not None:
                return winning_state

            depth_allowed += 1

    def dfs(self, max_depth):
        head = DFSNode(0, GameState(self.initial_board, None, None, None), None)
        if head.is_win():
            return head

        self.stack.append(head)

        while self.stack:
            current_node: DFSNode = self.stack.pop()
            if current_node.depth > max_depth:
                continue

            children = current_node.expand()
            for child in children:
                in_closed: DFSNode = self.closed.get(child.get_hash())
                if in_closed is None or child.depth < in_closed.depth:
                    # if child hasnt been processed yet
                    self.closed[child.get_hash()] = child
                    self.stack.append(child)

                if child.is_win():
                    return child
