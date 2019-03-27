from enum import Enum


class Direction(Enum):
    ROW = 1
    COL = 2


class MoveDirection(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def __str__(self):
        if self == self.RIGHT:
            return "RIGHT"
        if self == self.LEFT:
            return "LEFT"
        if self == self.UP:
            return "UP"
        if self == self.DOWN:
            return "DOWN"


def is_car_out_of_bounds(new_start_row, new_end_row, new_start_col, new_end_col):
    return new_end_col not in range(6) or new_start_col not in range(6) or new_end_row not in range(6) or new_start_row not in range(6)


class Car:

    def __init__(self, name, direction, start_row, start_col, end_row, end_col, length):
        self.name = name
        self.direction = direction
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.length = length

    def expected_location_after_move(self, move_direction, steps):
        if not self.is_move_logical(move_direction):
            raise Exception("Car.expected_location illogical move: attempted to move {} but car is {}".format(move_direction, self.direction))
        new_start_row = self.start_row
        new_end_row = self.end_row
        new_start_col = self.start_col
        new_end_col = self.end_col
        if move_direction in [MoveDirection.LEFT, MoveDirection.UP]:
            steps = -steps
        if self.direction == Direction.ROW:
            new_start_col += steps
            new_end_col += steps
        elif self.direction == Direction.COL:
            new_start_row += steps
            new_end_row += steps

        if is_car_out_of_bounds(new_start_row, new_end_row, new_start_col, new_end_col):
            raise Exception("expected_location_after_move: Car moved too much!")
        return new_start_row, new_end_row, new_start_col, new_end_col

    def is_move_logical(self, move_direction):
        if self.direction == Direction.ROW and move_direction in [MoveDirection.LEFT, MoveDirection.RIGHT]:
            return True
        if self.direction == Direction.COL and move_direction in [MoveDirection.UP, MoveDirection.DOWN]:
            return True
        return False

    def __str__(self):
        return "Car<({}){}: {}, ({}, {}), ({}, {})>".format(self.length, self.name, self.direction, self.start_row, self.start_col, self.end_row, self.end_col)


class Board:

    def __init__(self, game_data):
        self.game_board = Board.convert_data(game_data)
        self.cars_information = {}
        self.get_cars_info()
        self.red_car_info = self.cars_information.get('X')
        self.game_board_as_string = ''.join(self.game_board)

    @staticmethod
    def convert_data(game_data):
        return [game_data[start:start + 6] for start in range(0, len(game_data), 6)]

    def infer_car_length(self, direction, row, col):
        if row >= 6 or row < 0:
            raise IndexError("infer_car_length received out of Bounds parameters")
        if self.game_board[row][col] == '.':
            raise Exception("infer_car_length received non-car object on ({}, {}) was: {}".format(row, col, '\'.\''))
        length = 0
        if direction == Direction.COL:
            length = self.get_car_length_in_column(row, col)
        elif direction == Direction.ROW:
            length = self.get_car_length_in_row(row, col)
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
                if current_char == '.' or current_char in self.cars_information.keys():
                    continue
                if current_char == next_char:
                    current_car_length = self.infer_car_length(Direction.ROW, row, col)
                    addition = current_car_length - 1
                    self.cars_information[current_char] = Car(current_char, Direction.ROW, row, col, row, col + addition, current_car_length)

    def save_cars_in_cols(self):
        for row in range(5):
            for col in range(6):
                current_char = self.game_board[row][col]
                next_char = self.game_board[row + 1][col]
                if current_char == '.' or current_char in self.cars_information.keys():
                    continue
                if current_char == next_char:
                    current_car_length = self.infer_car_length(Direction.COL, row, col)
                    addition = current_car_length - 1
                    self.cars_information[current_char] = Car(current_char, Direction.COL, row, col, row + addition, col, current_car_length)

    def get_cars_info(self):
        self.save_cars_in_rows()
        self.save_cars_in_cols()

    def get_car_length_in_column(self, row, col):
        length = 1
        current_character = self.game_board[row][col]
        if row + 1 < 6 and current_character == self.game_board[row + 1][col]:
            length += 1
            if row + 2 < 6 and current_character == self.game_board[row + 2][col]:
                length += 1
        if row - 1 >= 0 and current_character == self.game_board[row - 1][col]:
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
        if col - 1 >= 0 and current_character == self.game_board[row][col - 1]:
            length += 1
            if col - 2 >= 0 and current_character == self.game_board[row][col - 2]:
                length += 1
        return length

    def move_car(self, car_name, move_side, steps):
        if steps < 0:
            raise Exception("move_car: Do not send negative steps")
        if move_side in [MoveDirection.LEFT, MoveDirection.UP]:
            steps = -steps
        if self.is_legal_move(car_name, steps) == False:
            return False
        self.do_the_move(car_name, steps)
        return True

    def is_legal_move(self, car_name, steps):
        _steps = abs(steps)
        if steps == 0:
            return False
        car_info: Car = self.cars_information.get(car_name)
        if car_info.direction == Direction.ROW:
            # going right
            end_col = car_info.end_col
            sign = 1
            # going left
            if steps < 0:
                end_col = car_info.start_col
                sign = -1
            for i in range(1, _steps + 1):
                i = i*sign
                if end_col + i < 0 or end_col + i >=6:
                    return False
                if self.game_board[car_info.start_row][end_col + i] != '.':
                    return False
            return True
        if car_info.direction == Direction.COL:
            # going down
            end_row = car_info.end_row
            sign = 1
            # going up
            if steps < 0:
                end_row = car_info.start_row
                sign = -1
            for i in range(1, _steps + 1):
                i = i*sign
                if end_row + i >= 6 or end_row + i < 0:
                    return False
                if self.game_board[end_row + i][car_info.start_col] != '.':
                    return False
            return True
        raise Exception("Incorrect value for car_info.direction was: {}".format(car_info.direction))

    # no indexExceptions should occur in this function
    def do_the_move(self, car_name, steps):
        _steps = abs(steps)
        car_info: Car = self.cars_information.get(car_name)
        if car_info.direction == Direction.ROW:
            #going right
            car_len = abs(car_info.length)
            end_col = car_info.end_col
            sign = 1
            # going left
            if steps < 0:
                end_col = car_info.start_col
                car_len = -car_len
                sign = -1
            for i in range(1, _steps + 1):
                i = i*sign
                self.replace_str(car_info.start_row, end_col + i, car_name)
                self.replace_str(car_info.start_row, end_col + i - car_len, '.')
            self.game_board_as_string = ''.join(self.game_board)
            self.cars_information[car_name] = Car(car_name, Direction.ROW, car_info.start_row, car_info.start_col + steps, car_info.end_row, car_info.end_col + steps, abs(car_len))
        elif car_info.direction == Direction.COL:
            # going down
            end_row = car_info.end_row
            sign = 1
            car_len = abs(car_info.length)
            # going up
            if steps < 0:
                end_row = car_info.start_row
                car_len = -car_len
                sign = -1
            for i in range(1, _steps + 1):
                i = i*sign
                self.replace_str(end_row + i, car_info.start_col, car_name)
                self.replace_str(end_row + i - car_len, car_info.start_col, '.')
            self.game_board_as_string = ''.join(self.game_board)
            self.cars_information[car_name] = Car(car_name, Direction.COL, car_info.start_row + steps, car_info.end_col , car_info.end_row + steps, car_info.end_col, abs(car_len))

    def replace_str(self, row, col, new_char):
        tmp = list(self.game_board[row])
        tmp[col] = new_char
        self.game_board[row] = ''.join(tmp)
        pass
