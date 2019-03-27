import sys

UNDEFINED_F_VALUE = -100
INFINITY = sys.maxsize - 100

class TODO:
    def __init__(self, msg=""):
        raise Exception("{\n\tTODO: " + msg + "\n}")


class HeuristicFunctionExplanations:
    # instantiate this class if you want an explanation for heuristics:
    def __init__(self):
        print("-----------------------------------------------------------------------------")
        print("Heuristic Functions:\t\t\t\t\t\t\t\t\t\t\t\t\t\t|")
        print("1: The amount of cars infront of the red car.\t\t\t\t\t\t\t\t|")
        print("2: The amount of cars that cover the third row.\t\t\t\t\t\t\t\t|")
        print("3: DLS.\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t|")
        print("4: The amount of cars that cover the third row, infront of the red car.\t\t|")
        print("-----------------------------------------------------------------------------")


def str_to_int(msg: str):
    return int(float(msg))


def display_colored_text(color, text):
    colored_text = f"\033[{color}{text}\033[00m"
    return colored_text
