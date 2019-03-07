from enum import Enum


class Direction(Enum):
    ROW = 1
    COL = 2


class Board:
    # 2 dimensional array
    game_board = []
    carsInformation = {}

    @staticmethod
    def convert_data(game_data):
        return [game_data[start:start + 6] for start in range(0, len(game_data), 6)]

    @staticmethod
    def get_car_length_by_character(char):
        if char in ['A', 'B', 'C', 'X']:
            return 2
        elif char in ['O', 'P', 'Q', 'R']:
            return 3
        elif char == '.':
            return 1
        return 0

    def go_through_rows(self):
        for row in range(6):
            for col in range(5):
                current_char = self.game_board[row][col]
                next_char = self.game_board[row][col + 1]
                if current_char == '.' or current_char in self.carsInformation.keys():
                    continue
                if current_char == next_char:
                    current_car_length = Board.get_car_length_by_character(current_char)
                    addition = current_car_length - 1
                    self.carsInformation[current_char] = [Direction.ROW, row, col, row, col + addition]

    def go_through_cols(self):
        for row in range(5):
            for col in range(6):
                current_char = self.game_board[row][col]
                next_char = self.game_board[row + 1][col]
                if current_char == '.' or current_char in self.carsInformation.keys():
                    continue
                if current_char == next_char:
                    current_car_length = Board.get_car_length_by_character(current_char)
                    addition = current_car_length - 1
                    self.carsInformation[current_char] = [Direction.ROW, row, col, row + addition, col]

    def get_cars_info(self):
        self.go_through_rows()
        self.go_through_cols()

    def __init__(self, game_data):
        self.game_board = Board.convert_data(game_data)
        self.carsInformation = {}
        self.get_cars_info()

