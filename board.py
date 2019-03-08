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

    def infer_car_length(self, direction, row, col):
        if row >= 6 or row < 0:
            raise IndexError("infer_car_length received out of Bounds parameters")
        length = 0
        if direction == Direction.COL:
            length = self.get_car_length_in_column(row, col)
        elif direction == Direction.ROW:
            length = self.get_car_length_in_row(row,col)
        else:
            raise Exception("infer_car_length received incorrect direction parameter. Was: {}".format(direction))

        if length == 1:
            raise Exception("infer_car_length attempted to return an incorrect car length of 1")
        return length

    def save_cars_in_rows(self):
        for row in range(6):
            for col in range(5):
                current_char = self.game_board[row][col]
                next_char = self.game_board[row][col + 1]
                if current_char == '.' or current_char in self.carsInformation.keys():
                    continue
                if current_char == next_char:
                    current_car_length = self.infer_car_length(Direction.ROW, row, col)
                    addition = current_car_length - 1
                    self.carsInformation[current_char] = [Direction.ROW, row, col, row, col + addition]

    def save_cars_in_cols(self):
        for row in range(5):
            for col in range(6):
                current_char = self.game_board[row][col]
                next_char = self.game_board[row + 1][col]
                if current_char == '.' or current_char in self.carsInformation.keys():
                    continue
                if current_char == next_char:
                    current_car_length = self.infer_car_length(Direction.COL, row, col)
                    addition = current_car_length - 1
                    self.carsInformation[current_char] = [Direction.ROW, row, col, row + addition, col]

    def get_cars_info(self):
        self.save_cars_in_rows()
        self.save_cars_in_cols()

    def __init__(self, game_data):
        self.game_board = Board.convert_data(game_data)
        self.carsInformation = {}
        self.get_cars_info()

    def get_car_length_in_column(self, row, col):
        length = 1
        current_character = self.game_board[row][col]
        if row + 1 < 6 and current_character == self.game_board[row + 1][col]:
            length += 1
            if row + 2 < 6 and current_character == self.game_board[row + 2][col]:
                length += 1
        elif row - 1 >= 0 and current_character == self.game_board[row - 1][col]:
            length += 1
            if row - 2 >= 0 and current_character == self.game_board[row - 2][col]:
                length+=1
        return length

    def get_car_length_in_row(self, row, col):
        length = 1
        current_character = self.game_board[row][col]
        if col + 1 < 6 and current_character == self.game_board[row][col + 1]:
            length += 1
            if col + 2 < 6 and current_character == self.game_board[row][col + 2]:
                length += 1
        elif col - 1 >= 0 and current_character == self.game_board[row][col - 1]:
            length += 1
            if col - 2 >= 0 and current_character == self.game_board[row][col - 2]:
                length += 1
        return length
