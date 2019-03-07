import sys

from board import Board


def display_colored_text(color, text):
    colored_text = f"\033[{color}{text}\033[00m"
    return colored_text


def read_input():
    try:
        file = sys.argv[1]
        timer = sys.argv[2]
    except IndexError:
        timer = 7
        file = './Data/rh.txt'

    with open(file, 'r') as f:
        contents = f.readlines()

    input_games = []
    i = contents.index('--- RH-input ---\n')
    for j in range(i + 1, contents.index('--- end RH-input ---\n')):
        input_games.append(contents[j].split('\n')[0])
    return input_games, timer


def convert_games(games_string_format):
    boards = []
    for game in games_string_format:
        boards.append(Board(game))
    return boards


def print_game_comfortably(game):
    for line in game.game_board:
        print(" ".join(line))


def main():

    input_games, timer = read_input()
    converted_games = convert_games(input_games)
    print_game_comfortably(converted_games[0])
    print(converted_games[0].carsInformation)
    print(len(converted_games[0].carsInformation))


if __name__ == '__main__':
    # try:
        main()
    # except IndexError:
    #     red = '31m'
    #     print(display_colored_text(red, "Err: Did you initiate the program correctly?"))
    #     print(display_colored_text(red, "Usage: python [main file name] [input games] [timeout]"))
    #     print(display_colored_text(red, "Example: python game.py ./Data/rh.txt 7"))
