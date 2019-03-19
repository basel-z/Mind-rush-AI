# import cProfile, pstats, io
# from pstats import SortKey

import sys

from board_tests import *
from moves_history import *
from DepthLimitedSearch import *

IS_DEBUGGING = 0
HEURISTIC_FUNCTION = 2


class HeuristicFunctionException(Exception):
    pass


def display_colored_text(color, text):
    colored_text = f"\033[{color}{text}\033[00m"
    return colored_text


def read_input(debugging):
    try:
        file = sys.argv[1]
        allocated_time = sys.argv[2]
        x = 0
        for char in allocated_time:
            x = x * 10 + (ord(char) - ord('0'))
        allocated_time = x
        print(allocated_time)
        heuristic_function = ord(sys.argv[3]) - ord('0')
        if heuristic_function not in [1, 2, 3]:
            raise HeuristicFunctionException("Incorrect Heurstic function entered, was: {}".format(heuristic_function))
    except IndexError:
        if debugging == 1:
            # default values for debugging
            file = './Data/rh.txt'
            allocated_time = 150
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
        print(display_colored_text(yellow, "Notice: heuristic = 1 checks number of cars blocking the red one from exiting"))
        print(display_colored_text(yellow, "Notice: heuristic = 2 checks number of cars blocked on the red car row"))
        print(display_colored_text(red, e))
        exit(1)

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


def run_a_star_algorithm(actual_games, heuristic_function, timer):
    start_time = time.time()
    f = open("output.txt", "w")
    f.write("")
    for i in range(0, 40):
        AStarAlgorithm(actual_games[i], heuristic_function, timer, i+1)
    # print("it's done, total time:")
    f.write('total time :{}'.format(time.time()-start_time))


def run_dls(actual_games, timer):
    start_time = time.time()
    f = open("output.txt", "w")
    for i in range(0, 40):
        DepthLimitedSearch(actual_games[i], i+1, timer)
    f.write('\ntotal time '.format(time.time() - start_time))

def main():
    input_games, timer, heuristic_function = read_input(IS_DEBUGGING)
    actual_games = convert_games(input_games)
    timer = float(timer)
    if heuristic_function == 1 or heuristic_function == 2:
        run_a_star_algorithm(actual_games, heuristic_function, timer)
    else:
         run_dls(actual_games, timer)


if __name__ == '__main__':
    # pr = cProfile.Profile()
    # pr.enable()
    main()
    # pr.disable()
    # sortBy = SortKey.CUMULATIVE
    # ps = pstats.Stats(pr).sort_stats(sortBy)
    # ps.print_stats()
