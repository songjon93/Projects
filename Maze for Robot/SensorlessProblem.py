from Maze import Maze
from time import sleep

class SensorlessProblem:
    def __init__(self, maze, goal_location=None):
        self.maze = maze
        self.goal_location = goal_location
        self.start_state = tuple()
        i = 0
        for y in range(0, maze.height):
            for x in range(0, maze.width):
                i += 1
                self.start_state += (maze.is_floor(x, y),)

    ## You write the good stuff here:

    def __str__(self):
        string =  "Blind robot problem: "
        return string

    def is_ob(self, state, x, y, direction):
        index = x + (y * self.maze.width)
        if not self.start_state[index]:
            return True
        # print("x = " + str(x + direction[0]) + " y = " + str(y + direction[1]))
        new_x = x + direction[0]
        new_y = y + direction[1]
        if new_x < 0 or new_x >= self.maze.width or new_y < 0 or new_y >= self.maze.height:
            return True
        return not self.start_state[index + direction[0] + (direction[1] * self.maze.width)]


    def is_collision(self, state, x, y, direction):
        index = x + (y * self.maze.width)
        return not state[index + direction[0] + (direction[1] * self.maze.width)]

    def move(self, state, direction):
        new_state = tuple()
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                index = x + (y * self.maze.width)

                if self.is_ob(state, x, y, [-1 * direction[0], -1 * direction[1]])\
                        or self.is_collision(state, x, y, [-1 * direction[0], -1 * direction[1]]):
                    if self.is_ob(state, x, y, direction):
                        new_state += (state[index],)
                    else:
                        new_state += (False,)
                else:
                    if self.start_state[index]:
                        new_state += (state[index - direction[0] - (direction[1] * self.maze.width)],)
                    else:
                        new_state += (False,)

        return new_state

    def get_successors(self, state):
        successors = []
        for i in range(-1, 2, 2):
            x = self.move(state, [i, 0])
            y = self.move(state, [0, i])
            successors.append(x), successors.append(y)
        return successors

    def is_goal(self, state):
        goal_state = tuple()

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if x == self.goal_location[0] and y == self.goal_location[1]:
                    goal_state += (True,)
                else:
                    goal_state += (False,)
        return state == goal_state

    # def is_goal(self, state):
    #     goal_state = 0
    #
    #     for y in range(self.maze.height):
    #         for x in range(self.maze.width):
    #             if state[x + (y * self.maze.width)]:
    #                 goal_state += 1
    #     print(goal_state)
    #     return goal_state == 1

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def update_loc(self, state):
        self.maze.robotloc = []
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                index = x + (y * self.maze.width)
                if state[index]:
                    self.maze.robotloc.extend([x,y])

    def animate_path(self, path):
        # reset the robot locations in the maze

        for state in path:

            s = ""
            for y in range(self.maze.height - 1, -1, -1):
                for x in range(self.maze.width):
                    if state[x + (y * self.maze.width)]:
                        s += "o"
                    elif not self.maze.is_floor(x, y):
                        s += "#"
                    else:
                        s += "x"
                s += "\n"

            print(s)
            sleep(1/2)

    def heuristic(self, state):
        states = []
        unique_x = set()
        unique_y = set()
        distance = 0
        maxim = 0
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                index = x + (y * self.maze.width)
                if state[index]:
                    if x not in unique_x:
                        unique_x.add(x)
                    if y not in unique_y:
                        unique_y.add(y)
                    states.append([x, y])

        return len(unique_y) + len(unique_x)

## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze1.maz")
    test_problem = SensorlessProblem(test_maze3, (2, 2))
    print(test_problem.start_state)
    print(test_problem.get_successors([False, False, False, False, False, False, True, True, False, False, True, False]))


