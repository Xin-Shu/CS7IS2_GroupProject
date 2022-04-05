import argparse
import sys
from scripts.sudoku import Sudoku
from scripts.ac3 import AC3
from scripts.backtrack import recursive_backtrack_algorithm
from scripts.utils import fetch_sudokus, print_grid
import numpy as np

"""
default sudokus' grid
"""
sudokus = dict(
    easy="000079065000003002005060093340050106000000000608020059950010600700600000820390000",
    medium="102004070000902800009003004000240006000107000400068000200800700007501000080400109",
    hard="002008050000040070480072000008000031600080005570000600000960048090020000030800900")

"""
solve
solves a sudoku based on its String grid
"""


def solve(grid, index, total):
    # print("\nSudoku {}/{} : \n{}".format(index, total, print_grid(grid)))

    # print("{}/{} : AC3 starting".format(index, total))

    # instanciate Sudoku
    sudoku = Sudoku(grid)
    list_of_intermediate_state = []
    # launch AC-3 algorithm of it
    AC3_result = AC3(sudoku, list_of_intermediate_state, queue=None)

    # Sudoku has no solution
    if not AC3_result:
        pass

    else:

        # check if AC-3 algorithm has solve the Sudoku
        # print("{}/{} : Result: \n{}".format(index, total, sudoku))
        if sudoku.isFinished():

            # print("{}/{} : AC3 was enough to solve this sudoku !".format(index,total))
            # print("{}/{} : Result: \n{}".format(index, total, sudoku))
            return list_of_intermediate_state[-1]

        # continue the resolution
        else:
            # print("{}/{} : AC3 finished, Backtracking starting...".format(index,total))

            assignment = {}

            # for the already known values
            for cell in sudoku.cells:

                if len(sudoku.possibilities[cell]) == 1:
                    assignment[cell] = sudoku.possibilities[cell][0]

            # start backtracking
            assignment = recursive_backtrack_algorithm(assignment, sudoku, list_of_intermediate_state)

            # merge the computed values for the cells at one place
            for cell in sudoku.possibilities:
                sudoku.possibilities[cell] = assignment[cell] if len(cell) > 1 else sudoku.possibilities[cell]

            if assignment:
                # print("{}/{} : Result: \n{}".format(index, total, sudoku))
                return list_of_intermediate_state[-1]

            else:
                pass


if __name__ == "__main__":

    # argument parsing using argparse module
    # doc @ https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='Solve a Sudoku with CSP')
    parser.add_argument('--string', type=str,
                        help='sudoku as a String, can be multiple sudokus in a row in the same line')
    parser.add_argument('--level', type=str, default='medium', choices=['easy', 'medium', 'hard'],
                        help='selects default sudoku\'s based on level (default: %(default)s)')
    args = parser.parse_args()

    sudoku_grid_as_string = ""

    # if user didnt provide a custom string or its string has not the right format
    if not args.string:

        # let's use the level's default
        sudoku_grid_as_string = sudokus[args.level]
        # print("\nUsing default sudoku, level : {}".format(args.level))

    else:

        sudoku_grid_as_string = args.string

    # fetch sudokus from user input
    sudoku_queue = fetch_sudokus(sudoku_grid_as_string)

    # for each sudoku, solve it !
    for index_, sudoku_grid in enumerate(sudoku_queue):
        solve(sudoku_grid, index_ + 1, len(sudoku_queue))


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string  
    for i in range(9):
        for j in range(9):
            str1 += s[i][j]
    sudoku_queue = fetch_sudokus(str1)

    # return string
    return sudoku_queue


def list_split(listA, n):
    for x in range(0, len(listA), n):
        every_chunk = listA[x: n + x]

        if len(every_chunk) < n:
            every_chunk = every_chunk + \
                          [None for y in range(n - len(every_chunk))]
        yield every_chunk
