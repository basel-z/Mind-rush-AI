# Note: This file is a test for board.py
from board import *


class BoardTest:

    @staticmethod
    def display_colored_text(color, text):
        colored_text = f"\033[{color}{text}\033[00m"
        return colored_text

    def __init__(self, actual_games_list):

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
        # self.test_function_move_car(board)
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
        board.is_legal_move()
        pass
