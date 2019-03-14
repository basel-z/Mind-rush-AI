# Note: This file is a test for board.py
from board import *


class BoardTest:

    @staticmethod
    def display_colored_text(color, text):
        colored_text = f"\033[{color}{text}\033[00m"
        return colored_text

    def __init__(self, actual_games_list):

        self.first_level_original_board = ["AA...O", "P..Q.O", "PXXQ.O", "P..Q..", "B...CC", "B.RRR."]
        self.green_highlight = '42m'
        self.green_color = '32m'
        self.run_test_on_first_level(actual_games_list[0])
        message = BoardTest.display_colored_text(self.green_highlight, "Success! All tests passed without error.")
        print(message)

    def run_test_on_first_level(self, board: Board):
        # try legal moves
        self.attempt_legal_moves_on_first(board)
        # try illegal moves
        # self.attempt_illegal_moves_on_first(board)
        # try combination
        # self.attempt_combination_of_legal_and_illegal_moves_on_first(board)

    def attempt_legal_moves_on_first(self, board):
        self.test_function_infer_car_length(board)
        self.test_function_is_legal_move(board)
        self.test_function_move_car(board)
        pass

    @staticmethod
    def test_function_infer_car_length(board):
        # logical usage:
        assert board.infer_car_length(Direction.ROW, 0, 0) == 2
        assert board.infer_car_length(Direction.ROW, 0, 1) == 2
        assert board.infer_car_length(Direction.ROW, 2, 1) == 2
        assert board.infer_car_length(Direction.ROW, 2, 2) == 2
        assert board.infer_car_length(Direction.ROW, 4, 4) == 2
        assert board.infer_car_length(Direction.ROW, 4, 5) == 2
        assert board.infer_car_length(Direction.ROW, 5, 2) == 3
        assert board.infer_car_length(Direction.ROW, 5, 3) == 3
        assert board.infer_car_length(Direction.ROW, 5, 4) == 3

        assert board.infer_car_length(Direction.COL, 1, 0) == 3
        assert board.infer_car_length(Direction.COL, 2, 0) == 3
        assert board.infer_car_length(Direction.COL, 3, 0) == 3
        assert board.infer_car_length(Direction.COL, 4, 0) == 2
        assert board.infer_car_length(Direction.COL, 5, 0) == 2
        assert board.infer_car_length(Direction.COL, 1, 3) == 3
        assert board.infer_car_length(Direction.COL, 2, 3) == 3
        assert board.infer_car_length(Direction.COL, 3, 3) == 3
        assert board.infer_car_length(Direction.COL, 0, 5) == 3
        assert board.infer_car_length(Direction.COL, 1, 5) == 3
        assert board.infer_car_length(Direction.COL, 2, 5) == 3

        # finding lengths of '.'
        num_of_exceptions_caught = 0
        try:
            board.infer_car_length(Direction.ROW, 0, 3)
        except Exception:
            num_of_exceptions_caught += 1
        try:
            board.infer_car_length(Direction.COL, 0, 3)
        except Exception:
            num_of_exceptions_caught += 1

        assert num_of_exceptions_caught == 2

        # flipped usage of ROW/COL:
        num_of_exceptions_caught = 0
        try:
            assert board.infer_car_length(Direction.COL, 0, 0) == 2
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.COL, 0, 1) == 2
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.COL, 2, 1) == 2
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.COL, 2, 2) == 2
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.COL, 4, 4) == 2
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.COL, 4, 5) == 2
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.COL, 5, 2) == 3
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.COL, 5, 3) == 3
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.COL, 5, 4) == 3
        except Exception:
            num_of_exceptions_caught += 1

        try:
            assert board.infer_car_length(Direction.ROW, 1, 0) == 3
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.ROW, 2, 0) == 3
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.ROW, 3, 0) == 3
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.ROW, 4, 0) == 2
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.ROW, 5, 0) == 2
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.ROW, 1, 3) == 3
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.ROW, 2, 3) == 3
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.ROW, 3, 3) == 3
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.ROW, 0, 5) == 3
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.ROW, 1, 5) == 3
        except Exception:
            num_of_exceptions_caught += 1
        try:
            assert board.infer_car_length(Direction.ROW, 2, 5) == 3
        except Exception:
            num_of_exceptions_caught += 1

        assert num_of_exceptions_caught == 20

    @staticmethod
    def test_function_is_legal_move(board):

        assert board.is_legal_move("A", 1) == True
        assert board.is_legal_move("A", 2) == True
        assert board.is_legal_move("A", 3) == True
        assert board.is_legal_move("A", 4) == False
        assert board.is_legal_move("A", 5) == False
        assert board.is_legal_move("A", 6) == False
        assert board.is_legal_move("A", -1) == False
        assert board.is_legal_move("A", -2) == False
        assert board.is_legal_move("A", -3) == False
        assert board.is_legal_move("A", -4) == False
        assert board.is_legal_move("A", -5) == False
        assert board.is_legal_move("A", -6) == False

        assert board.is_legal_move("P", 1) == False
        assert board.is_legal_move("P", 2) == False
        assert board.is_legal_move("P", 3) == False
        assert board.is_legal_move("P", 4) == False
        assert board.is_legal_move("P", 5) == False
        assert board.is_legal_move("P", 6) == False
        assert board.is_legal_move("P", -1) == False
        assert board.is_legal_move("P", -2) == False
        assert board.is_legal_move("P", -3) == False
        assert board.is_legal_move("P", -4) == False
        assert board.is_legal_move("P", -5) == False
        assert board.is_legal_move("P", -6) == False

        assert board.is_legal_move("B", 1) == False
        assert board.is_legal_move("B", 2) == False
        assert board.is_legal_move("B", 3) == False
        assert board.is_legal_move("B", 4) == False
        assert board.is_legal_move("B", 5) == False
        assert board.is_legal_move("B", 6) == False
        assert board.is_legal_move("B", -1) == False
        assert board.is_legal_move("B", -2) == False
        assert board.is_legal_move("B", -3) == False
        assert board.is_legal_move("B", -4) == False
        assert board.is_legal_move("B", -5) == False
        assert board.is_legal_move("B", -6) == False

        assert board.is_legal_move("X", 1) == False
        assert board.is_legal_move("X", 2) == False
        assert board.is_legal_move("X", 3) == False
        assert board.is_legal_move("X", 4) == False
        assert board.is_legal_move("X", 5) == False
        assert board.is_legal_move("X", 6) == False
        assert board.is_legal_move("X", -1) == False
        assert board.is_legal_move("X", -2) == False
        assert board.is_legal_move("X", -3) == False
        assert board.is_legal_move("X", -4) == False
        assert board.is_legal_move("X", -5) == False
        assert board.is_legal_move("X", -6) == False

        assert board.is_legal_move("R", 1) == True
        assert board.is_legal_move("R", 2) == False
        assert board.is_legal_move("R", 3) == False
        assert board.is_legal_move("R", 4) == False
        assert board.is_legal_move("R", 5) == False
        assert board.is_legal_move("R", 6) == False
        assert board.is_legal_move("R", -1) == True
        assert board.is_legal_move("R", -2) == False
        assert board.is_legal_move("R", -3) == False
        assert board.is_legal_move("R", -4) == False
        assert board.is_legal_move("R", -5) == False
        assert board.is_legal_move("R", -6) == False

        assert board.is_legal_move("Q", 1) == True
        assert board.is_legal_move("Q", 2) == False
        assert board.is_legal_move("Q", 3) == False
        assert board.is_legal_move("Q", 4) == False
        assert board.is_legal_move("Q", 5) == False
        assert board.is_legal_move("Q", 6) == False
        assert board.is_legal_move("Q", -1) == True
        assert board.is_legal_move("Q", -2) == False
        assert board.is_legal_move("Q", -3) == False
        assert board.is_legal_move("Q", -4) == False
        assert board.is_legal_move("Q", -5) == False
        assert board.is_legal_move("Q", -6) == False

        assert board.is_legal_move("C", 1) == False
        assert board.is_legal_move("C", 2) == False
        assert board.is_legal_move("C", 3) == False
        assert board.is_legal_move("C", 4) == False
        assert board.is_legal_move("C", 5) == False
        assert board.is_legal_move("C", 6) == False
        assert board.is_legal_move("C", -1) == True
        assert board.is_legal_move("C", -2) == True
        assert board.is_legal_move("C", -3) == True
        assert board.is_legal_move("C", -4) == False
        assert board.is_legal_move("C", -5) == False
        assert board.is_legal_move("C", -6) == False

        assert board.is_legal_move("O", 1) == True
        assert board.is_legal_move("O", 2) == False
        assert board.is_legal_move("O", 3) == False
        assert board.is_legal_move("O", 4) == False
        assert board.is_legal_move("O", 5) == False
        assert board.is_legal_move("O", 6) == False
        assert board.is_legal_move("O", -1) == False
        assert board.is_legal_move("O", -2) == False
        assert board.is_legal_move("O", -3) == False
        assert board.is_legal_move("O", -4) == False
        assert board.is_legal_move("O", -5) == False
        assert board.is_legal_move("O", -6) == False

    @staticmethod
    def opposite_move_direction(current_move_direction: MoveDirection):
        if current_move_direction == MoveDirection.UP:
            return MoveDirection.DOWN
        elif current_move_direction == MoveDirection.DOWN:
            return MoveDirection.UP
        elif current_move_direction == MoveDirection.LEFT:
            return MoveDirection.RIGHT
        elif current_move_direction == MoveDirection.RIGHT:
            return MoveDirection.LEFT
        raise Exception("Tests failed! opposite_move_direction received an incorrect direction was: {}".format(current_move_direction))

    @staticmethod
    def move_and_return_to_base(c, board, car_name, move_side, steps, expected_board):
        original_board = board.game_board.copy()
        board.move_car(car_name, move_side, steps)
        success1 = board.game_board == expected_board
        opposite_side = BoardTest.opposite_move_direction(move_side)
        board.move_car(car_name, opposite_side, steps)
        success2 = board.game_board == original_board
        if not success1:
            raise Exception("Failed to move car as expected! on call number: {}".format(c))
        if not success2:
            raise Exception("Failed to get back to original as expected! on call number: {}".format(c))
        return c + 1

    @staticmethod
    def test_function_move_car(board):
        c = 0
        c = BoardTest.move_and_return_to_base(c, board, "A", MoveDirection.RIGHT, 1, [".AA..O", "P..Q.O", "PXXQ.O", "P..Q..", "B...CC", "B.RRR."])

