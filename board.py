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

    def get_cars_info(self):
        for i in range(6):
            for j in range(5):
                character = self.game_board[i][j]
                if self.game_board[i][j+1] == character:
                    if character in ['A', 'B', 'C', 'X']:
                        self.carsInformation[character] = [Direction.ROW, i, j, i, j+1]
                    elif self.game_board[i][j+1] in ['O', 'P', 'Q', 'R']:
                        self.carsInformation[character] = [Direction.ROW, i, j, i, j+2]
                        j += 1
        #
        # for j in range(5):
        #     for i in range(6):
        #         character = self.game_board[i][j]
        #         if self.game_board[i+1][j] == character:
        #             if character in ['A', 'B', 'C', 'X']:
        #                 self.carsInformation[character] = [Direction.COL, i, j, i+1, j]
        #             elif self.game_board[i+1][j] in ['O', 'P', 'Q', 'R']:
        #                 self.carsInformation[character] = [Direction.COL, i, j, i+2, j]
        #                 i += 1

    def __init__(self, game_data):
        self.game_board = Board.convert_data(game_data)
        self.get_cars_info()

