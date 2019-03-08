from enum import Enum


class Direction(Enum):
    ROW = 1
    COL = 2


class MoveDirection(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


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

    def move_car(self, car_name, move_side, steps):
        if move_side in [MoveDirection.DOWN, MoveDirection.LEFT]:
            steps = -steps
        if self.is_legal_move(car_name, steps) == False:
            return False
        self.do_the_move(car_name, steps)

    def is_legal_move(self, car_name, steps):
        _steps = abs(steps)
        car_info = self.carsInformation.get(car_name)
        if car_info[0] == Direction.ROW:
            end_col = car_info[4]
            for i in range(_steps):
                i += 1
                if _steps + i > 6:
                    return False
                if steps < 0:
                    i = -i
                    end_col = car_info[2]
                if self.game_board[car_info[1]][end_col + i] != '.':
                    return False
            return True
        if car_info[0] == Direction.COL:
            end_row = car_info[1]
            for i in range(_steps):
                i += 1
                if _steps + i > 6:
                    return False
                if steps < 0:
                    i = -i
                    end_row = car_info[3]
                if self.game_board[end_row + i][car_info[2]] != '.':
                    return False
            return True

    def do_the_move(self, car_name, steps):
        _steps = abs(steps)
        car_info = self.carsInformation.get(car_name)
        if car_info[0] == Direction.ROW:
            end_col = car_info[4]
            for i in range(_steps):
                i += 1
                if steps < 0:
                    i = -i
                    end_col = car_info[2]
                tmp = list(self.game_board[car_info[1]])
                tmp[end_col + i] = car_name
                self.game_board[car_info[1]] = ''.join(tmp)
            car_len = car_info[4] - car_info[2] + 1
            if steps < car_len:
                cells_to_empty = car_len-_steps
            else:
                cells_to_empty = car_len
            for i in range(cells_to_empty):
                # i += 1
                tmp = list(self.game_board[car_info[1]])
                if steps > 0:
                    tmp[car_info[2] + i] = '.'
                else:
                    tmp[car_info[4] - i] = '.'
                self.game_board[car_info[1]] = ''.join(tmp)
            self.carsInformation[car_name] = [Direction.ROW, car_info[1], car_info[2] + steps, car_info[1], car_info[4] + steps]




        if car_info[0] == Direction.COL:
            end_row = car_info[4]
            for i in range(_steps):
                i += 1
                if steps < 0:
                    i = -i
                    end_row = car_info[2]
                tmp = list(self.game_board[car_info[2]])
                tmp[end_col + i] = car_name
                self.game_board[car_info[1]] = ''.join(tmp)
            car_len = car_info[4] - car_info[2] + 1
            if steps < car_len:
                cells_to_empty = car_len - _steps
            else:
                cells_to_empty = car_len
            for i in range(cells_to_empty):
                # i += 1
                tmp = list(self.game_board[car_info[1]])
                if steps > 0:
                    tmp[car_info[2] + i] = '.'
                else:
                    tmp[car_info[4] - i] = '.'
                self.game_board[car_info[1]] = ''.join(tmp)
            self.carsInformation[car_name] = [Direction.ROW, car_info[1], car_info[2] + steps , car_info[1], car_info[4] + steps]
