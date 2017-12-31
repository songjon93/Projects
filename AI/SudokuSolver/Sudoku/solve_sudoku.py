from display import display_sudoku_solution
import random, sys
import time
from SAT import SAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(3)

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    sat = SAT(sys.argv[1])

    start_time = time.time()
    result = sat.walksat()
    # result = sat.gsat()
    end_time = time.time()

    print("Iteration : " + str(sat.iteration) + " times.")
    print("Time Elapsed : " + "%.2f" + " seconds") % (end_time - start_time)

    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)