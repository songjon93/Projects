from display import display_map_solution
import random, sys
from SAT import SAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    map_name = str(sys.argv[1][:-4])
    sol_filename = map_name + ".sol"

    sat = SAT(sys.argv[1])

    # result = sat.walksat()
    result = sat.gsat()
    if result:
        sat.write_solution(sol_filename)
        display_map_solution(sol_filename)