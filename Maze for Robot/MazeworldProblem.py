from Maze import Maze
from time import sleep

class MazeworldProblem:

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.start_state = (0, maze.robotloc[0], maze.robotloc[1])
        for i in range(2, len(maze.robotloc), 2):
            self.start_state += (maze.robotloc[i], maze.robotloc[i+1])

        self.goal_locations = goal_locations

    def __str__(self):
        string =  "Mazeworld problem: "
        return string

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1/2)

            print(str(self.maze))

    def update_loc(self, state):
        self.maze.robotloc = state[1:]

    # exists function checks if a given x, y coordinates already exist within the provided state.
    def exists(self, state, coordinate):
        for i in range(1, len(state), 2):
            if coordinate[0] == state[i] and coordinate[1] == state[i+1]:
                return True
        return False

    # get_successor function appends to a dictionary using the robot index as a keypossible states that can be
    # reached by each robot. And using that dictionary, it calls get_successor_helper function that recursively
    # compounds these possible states together and filters out illegal combinations
    def get_successors(self, state):
        robot_num = int(len(state)/2)
        possible_states = dict()

        for i in range(robot_num):
            possible_states[i] = [(state[i * 2 + 1], state[i * 2 + 2])]
            for move in range(-1, 2, 2):
                for vertical in range(0, 2):
                    robot_index = 1 + (2 * i)

                    if vertical and self.is_legal((state[robot_index] + move, state[robot_index + 1])):
                        possible_states[i].append((state[robot_index] + move, state[robot_index + 1]))

                    if not vertical and self.is_legal((state[robot_index], state[robot_index + 1] + move)):
                        possible_states[i].append((state[robot_index], state[robot_index + 1] + move))

        future_state = tuple() + (0,)
        successors = [state]
        self.get_successors_helper(successors, future_state, 0, robot_num, possible_states)
        return successors

    # every robot has 4 possible states (east, west, south, west), and the recursion makes it possible to look over
    # every possible combinations of these 4 states for k robots (which would be 4^k at max)
    def get_successors_helper(self, successors, state, robot_index, robot_num, possible_states):
        if robot_index >= robot_num:
            successors.append(state)
            return

        for i in possible_states[robot_index]:
            if not self.exists(state, i):
                criss_cross = False

                for j in range(1, len(state), 2):
                    if successors[0][j] == i[0] and successors[0][j + 1] == i[1]:
                        if state[j] == successors[0][robot_index * 2 + 1] and \
                                        state[j + 1] == successors[0][robot_index * 2 + 2] and (j-1)/2 != robot_index:
                            criss_cross = True

                if not criss_cross:
                    temp_state = state
                    temp_state += i
                    self.get_successors_helper(successors, temp_state, robot_index + 1,
                                                       robot_num, possible_states)

    def is_legal(self, state):
        x = state[0]
        y = state[1]

        if not self.maze.is_floor(x, y):
            return False

        return True

    def is_goal(self, state):
        return state[1:] == self.goal_locations

    def manhattan_heuristic(self, state):
        distance = 0
        for i in range(1, len(state)):
            distance += abs(self.goal_locations[i-1] - state[i])
        return distance