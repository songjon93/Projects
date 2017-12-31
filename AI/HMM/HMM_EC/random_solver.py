from HMM import HMM
from MazeGenerator import MazeGenerator

if __name__ == '__main__':
    file_name = "test_maze.maz"
    MazeGenerator(5, 7, file_name).generate_random_maze()
    test_maze = HMM(file_name)
    test_maze.simulate(10)
    print(test_maze.str_matrix())