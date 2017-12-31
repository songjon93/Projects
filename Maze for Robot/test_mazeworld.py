from MazeworldProblem import MazeworldProblem
from SensorlessProblem import SensorlessProblem
from Maze import Maze

# from uninformed_search import bfs_search
from astar_search import astar_search


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0


test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
test_sensor = SensorlessProblem(test_maze3, (2, 5))

# # this should do a bit better:
result = astar_search(test_mp, test_mp.manhattan_heuristic)

print(result)

test_mp.animate_path(result.path)

result = astar_search(test_sensor, test_sensor.heuristic)
print(result)

test_sensor.animate_path(result.path)
