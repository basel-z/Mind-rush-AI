# import cProfile, pstats, io
# from pstats import SortKey

import sys

from DepthLimitedSearch import *
from IDAStar import *
from board_tests import *
from doubleAStar import *
from moves_history import *
from utils import HeuristicFunctionExplanations, str_to_int, display_colored_text, AlgorithmType

IS_DEBUGGING = 1
HEURISTIC_FUNCTION = 1
DEBUGGING_ALGORITHM: AlgorithmType = AlgorithmType.IDA_STAR


class HeuristicFunctionException(Exception):
    pass


def int_to_algorithm_enum(algorithm_index):
    if algorithm_index == 1:
        return AlgorithmType.DLS
    if algorithm_index == 2:
        return AlgorithmType.A_STAR
    if algorithm_index == 3:
        return AlgorithmType.IDA_STAR
    if algorithm_index == 4:
        return AlgorithmType.BIDIRECTIONAL_A_STAR
    raise Exception("Attempted to access an incorrect algorithm number. Allowed: {}".format(AlgorithmType.MAX_ENUM_VALUE))


def read_input(debugging):
    try:
        file = sys.argv[1]
        allocated_time = str_to_int(sys.argv[2])
        heuristic_function = str_to_int(sys.argv[3])
        algorithm: AlgorithmType = AlgorithmType(int_to_algorithm_enum(str_to_int(sys.argv[4])))
        if heuristic_function not in [1, 2, 3, 4]:
            raise HeuristicFunctionException("Incorrect Heuristic function entered, was: {}".format(heuristic_function))
    except IndexError:
        if debugging == 1:
            # default values for debugging
            file = './Data/rh.txt'
            sol_file = './Data/sol.txt'
            allocated_time = 150
            heuristic_function = HEURISTIC_FUNCTION
            algorithm: AlgorithmType = DEBUGGING_ALGORITHM
            if heuristic_function not in [1, 2, 3, 4]:
                raise HeuristicFunctionException("Incorrect Heuristic function entered, was: {}".format(heuristic_function))
        else:
            red = '31m'
            print(display_colored_text(red, "Err: Did you initiate the program correctly?"))
            print(display_colored_text(red, "Usage: python [main file name] [input games] [timeout] [heuristic function 1/2/4, or 3(DLS)] [algorithm index 1-4]"))
            print(display_colored_text(red, "Example: python game.py ./Data/rh.txt 7 1"))
            yellow = '34m'
            print(display_colored_text(yellow, "Notice: heuristic = 1 checks number of cars blocking the red one from exiting"))
            print(display_colored_text(yellow, "Notice: heuristic = 2 checks number of cars blocked on the red car row"))
            exit(1)
    except HeuristicFunctionException as e:
        red = '31m'
        print(display_colored_text(red, "Err: Did you initiate the program correctly?"))
        print(display_colored_text(red, "Usage: python [main file name] [input games] [timeout] [heuristic function 1/2, or 3(DLS)]"))
        print(display_colored_text(red, "Example: python game.py ./Data/rh.txt 7 1"))
        yellow = '34m'
        print(display_colored_text(yellow, "Notice: heuristic = 1 checks number of cars blocking the red one from exiting"))
        print(display_colored_text(yellow, "Notice: heuristic = 2 checks number of cars blocked on the red car row"))
        print(display_colored_text(red, e))
        exit(1)

    with open(file, 'r') as f:
        contents = f.readlines()
    with open(sol_file, 'r') as f:
        sol_contents = f.readlines()
    for i in range(40):
        sol_contents[i] = sol_contents[i].split('\n')[0]

    input_games = []
    i = contents.index('--- RH-input ---\n')
    for j in range(i + 1, contents.index('--- end RH-input ---\n')):
        input_games.append(contents[j].split('\n')[0])
    return input_games, allocated_time, heuristic_function, algorithm, sol_contents


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
    f.write('total time :{}'.format(time.time()-start_time))


def run_dls(actual_games, timer):
    start_time = time.time()
    f = open("output.txt", "w")
    for i in range(0, 40):
        DepthLimitedSearch(actual_games[i], i+1, timer)
    # f.write('\ntotal time '.format(time.time() - start_time))


def run_double_a_star(actual_games, sol_games):
    # f = open("output.txt", "w")
    # f.write("")
    for i in range(0, 40):
        doubleAstar(actual_games[i], sol_games[i], 30, i+1)


def run_ida_star(actual_games, heuristic_function, allocated_time):
    f = open("output.txt", "w")
    f.write("")
    for i in range(0, 40):
        IDAStar(actual_games[i], i+1, heuristic_function, allocated_time)


def main():
    input_games, allocated_time, heuristic_function, algorithm, sol = read_input(IS_DEBUGGING)
    actual_games = convert_games(input_games)
    if algorithm == AlgorithmType.DLS:
        run_dls(actual_games, allocated_time)
    elif algorithm == AlgorithmType.A_STAR:
        run_a_star_algorithm(actual_games, heuristic_function, allocated_time)
    elif algorithm == AlgorithmType.IDA_STAR:
        run_ida_star(actual_games, heuristic_function, allocated_time)
    elif algorithm.value == AlgorithmType.BIDIRECTIONAL_A_STAR:
        run_double_a_star(actual_games, sol)


if __name__ == '__main__':
    # pr = cProfile.Profile()
    # pr.enable()
    HeuristicFunctionExplanations()
    main()
    # pr.disable()
    # sortBy = SortKey.CUMULATIVE
    # ps = pstats.Stats(pr).sort_stats(sortBy)
    # ps.print_stats()
