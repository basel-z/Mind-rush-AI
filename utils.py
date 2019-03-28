import sys
from enum import Enum

UNDEFINED_F_VALUE = -100
INFINITY = sys.maxsize - 100

F_INPUT_GAME_INPUT_FILE = "./Data/rh.txt"
F_INPUT_DOUBLE_A_STAR_BOARDS = "./Data/sol.txt"
F_INPUT_OPTIMAL_SOLUTIONS = "./Data/steps.txt"
F_OUTPUT_REINFORCEMENT_FILE = "./Output/output_reinforcement.txt"
F_OUTPUT_DOUBLE_A_STAR_FILE = "./Output/output_double_a_star.txt"
F_OUTPUT_IDA_STAR_FILE = "./Output/output_ida_star.txt"
F_OUTPUT_DLS_FILE = "./Output/output_dls.txt"
F_OUTPUT_A_STAR_FILE = "./Output/a_star.txt"

RED_TEXT = '31m'
GREEN_TEXT = '34m'
YELLOW_TEXT = '34m'
GREEN_HIGHLIGHT = '42m'

class TODO:
    def __init__(self, msg=""):
        raise Exception("{\n\tTODO: " + msg + "\n}")


class AlgorithmType(Enum):
    DLS = 1
    A_STAR = 2
    IDA_STAR = 3
    BIDIRECTIONAL_A_STAR = 4
    REINFORCEMENT_LEARNING = 5
    MAX_ENUM_VALUE = 5  # TODO: please keep this updated to the maximum available

    def __init__(self, a):
        self._value_ = a


class HeuristicFunctionExplanations:
    # instantiate this class if you want an explanation for heuristics:
    def __init__(self, debugging_algorithm):
        print("-----------------------------------------------------------------------------")
        print("Heuristic Functions:\t\t\t\t\t\t\t\t\t\t\t\t\t\t|")
        print("1: The amount of cars infront of the red car.\t\t\t\t\t\t\t\t|")
        print("2: The amount of cars that cover the third row.\t\t\t\t\t\t\t\t|")
        print("3: DLS.\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t|")
        print("4: The amount of cars that cover the third row, infront of the red car.\t\t|")
        print("-----------------------------------------------------------------------------")
        print("Algorithms to Run:\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t|")
        for current_type in AlgorithmType:
            current_type_as_string = "{}".format(current_type)
            current_type_as_string = current_type_as_string.replace("AlgorithmType.", "")
            tabs_to_append = ""
            to_print = "{}: {}".format(current_type._value_, current_type_as_string)
            num_of_spaces_to_add = 19 - int((len(to_print)/4))
            for i in range(0, num_of_spaces_to_add):
                tabs_to_append += "\t"
            to_print = to_print + tabs_to_append + "|"
            print(to_print)
        print("-----------------------------------------------------------------------------")
        algorithm_info = ""
        if debugging_algorithm is not None:
            algorithm_info = debugging_algorithm
        print(display_colored_text(RED_TEXT, "Running {}...".format(algorithm_info)))


def str_to_int(msg: str):
    return int(float(msg))


def display_colored_text(color, text):
    colored_text = f"\033[{color}{text}\033[00m"
    return colored_text
