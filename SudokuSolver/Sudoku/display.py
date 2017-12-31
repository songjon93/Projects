from Sudoku import Sudoku
import sys


def display_sudoku_solution(filename):

    test_sudoku = Sudoku()
    test_sudoku.read_solution(filename)
    print(test_sudoku)


def display_map_solution(filename):
    map_solution = open(filename, "r")
    for line in map_solution:
        val = line[0]
        if val != '-':
            print(line[:-2] + " is " + line[-2:])


if __name__ == "__main__":
    display_sudoku_solution(sys.argv[1])