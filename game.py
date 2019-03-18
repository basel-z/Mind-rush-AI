# import cProfile, pstats, io
# from pstats import SortKey

import sys

from board_tests import *
from moves_history import *

IS_DEBUGGING = 1
HEURISTIC_FUNCTION = 1


class HeuristicFunctionException(Exception):
    pass


def display_colored_text(color, text):
    colored_text = f"\033[{color}{text}\033[00m"
    return colored_text


def read_input(debugging):
    try:
        file = sys.argv[1]
        allocated_time = sys.argv[2]
        heuristic_function = sys.argv[3]
        if heuristic_function not in [1, 2]:
            raise HeuristicFunctionException("Incorrect Heurstic function entered, was: {}".format(heuristic_function))
    except IndexError:
        if debugging == 1:
            # default values for debugging
            file = './Data/rh.txt'
            allocated_time = 7
            heuristic_function = HEURISTIC_FUNCTION
            if heuristic_function not in [1, 2]:
                raise HeuristicFunctionException("Incorrect Heurstic function entered, was: {}".format(heuristic_function))
        else:
            red = '31m'
            print(display_colored_text(red, "Err: Did you initiate the program correctly?"))
            print(display_colored_text(red, "Usage: python [main file name] [input games] [timeout] [heuristic function 1/2]"))
            print(display_colored_text(red, "Example: python game.py ./Data/rh.txt 7 1"))
            yellow = '34m'
            print(display_colored_text(yellow, "Notice: heuristic = 1 checks number of cars blocking the red one from exiting"))
            print(display_colored_text(yellow, "Notice: heuristic = 2 checks number of cars blocked on the red car row"))
            exit(1)
    except HeuristicFunctionException as e:
        red = '31m'
        print(display_colored_text(red, "Err: Did you initiate the program correctly?"))
        print(display_colored_text(red, "Usage: python [main file name] [input games] [timeout] [heuristic function 1/2]"))
        print(display_colored_text(red, "Example: python game.py ./Data/rh.txt 7 1"))
        yellow = '34m'
        print(display_colored_text(yellow,"Notice: heuristic = 1 checks number of cars blocking the red one from exiting"))
        print(display_colored_text(yellow, "Notice: heuristic = 2 checks number of cars blocked on the red car row"))
        print(display_colored_text(red, e))

    with open(file, 'r') as f:
        contents = f.readlines()

    input_games = []
    i = contents.index('--- RH-input ---\n')
    for j in range(i + 1, contents.index('--- end RH-input ---\n')):
        input_games.append(contents[j].split('\n')[0])
    return input_games, allocated_time, heuristic_function


def convert_games(games_string_format):
    boards = []
    for game in games_string_format:
        boards.append(Board(game))
    return boards


def print_game_comfortably(game):
    for line in game.game_board:
        print(" ".join(line))
    print()
def run_tests(actual_games):
    BoardTest(actual_games)

def main():
    input_games, timer, heuristic_function = read_input(IS_DEBUGGING)
    actual_games = convert_games(input_games)
    start_time = time.time()
    for i in range(0, 40):
        print("game {} heuristic_function={}".format(i+1, heuristic_function))
        AStarAlgorithm(actual_games[i], heuristic_function)
        print('total time till now:{}', format(time.time()-start_time))
        print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("it's done, total time:")
    print(time.time()-start_time)
    # print_game_comfortably(actual_games[0])
    # actual_games[0].move_car('A', MoveDirection.RIGHT, 1)
    # actual_games[0].move_car('A', MoveDirection.LEFT, 1)
    # actual_games[0].move_car('O', MoveDirection.DOWN, 1)
    # actual_games[0].move_car('O', MoveDirection.UP, 1)
    # print_game_comfortably(actual_games[0])
    # run_tests(actual_games)
    # print_game_comfortably(actual_games[0])
    # print(actual_games[0].cars_information)
    # print("--------------------------------------")
    # print("Printing Cars:")
    # for car in actual_games[0].cars_information.values():
    #     print(car)
    # print("--------------------------------------")
    # print(len(actual_games[0].cars_information))
    # res = actual_games[0].move_car('C', MoveDirection.LEFT, 3)
    # assert (res == True)
    # print_game_comfortably(actual_games[0])
    # res = actual_games[0].move_car('A', MoveDirection.RIGHT, 1)
    # assert res == True
    # print_game_comfortably(actual_games[0])
    # res = actual_games[0].move_car('O', MoveDirection.DOWN, 6)
    # assert res == False
    # print_game_comfortably(actual_games[0])
    # res = actual_games[0].move_car('O', MoveDirection.DOWN, 2)
    # assert res == True
    # print_game_comfortably(actual_games[0])
    # AStarAlgorithm(actual_games[0], Car('X',Direction.ROW, 2, 1, 2, 2, 2))
    # AStarAlgorithm(actual_games[39], Car('X',Direction.ROW, 2, 3, 2, 4, 2))
    # AStarAlgorithm(actual_games[32], Car('X',Direction.ROW, 2, 3, 2, 4, 2))
    # AStarAlgorithm(actual_games[20], Car('X',Direction.ROW, 2, 1, 2, 2, 2))
    # AStarAlgorithm(actual_games[31], Car('X',Direction.ROW, 2, 0, 2, 1, 2))
    # AStarAlgorithm(actual_games[31], Car('X',Direction.ROW, 2, 0, 2, 1, 2))
    # AStarAlgorithm(actual_games[31], Car('X',Direction.ROW, 2, 0, 2, 1, 2))


if __name__ == '__main__':
    # pr = cProfile.Profile()
    # pr.enable()
    main()
    # pr.disable()
    # sortBy = SortKey.CUMULATIVE
    # ps = pstats.Stats(pr).sort_stats(sortBy)
    # ps.print_stats()
