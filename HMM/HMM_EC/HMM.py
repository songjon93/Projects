import numpy as np
import random
import time


class HMM:
    def __init__(self, file_name, initial_location=(-1, -1), move_sequence=[], get_seq=True):
        self.robotlocs = []
        self.get_seq = get_seq
        self.file_name = file_name
        self.lines = self.read_file()
        self.width = len(self.lines[0])
        self.height = len(self.lines)
        self.maze = self.build_maze()
        self.colors = ['r', 'g', 'b', 'y']
        self.sensor_accuracy = .88
        self.initial_loc = initial_location
        self.move_seq = move_sequence
        self.robotlocs = self.find_robotlocs()
        self.color_sequence = self.get_color_seq()
        self.floor_count = self.count_floors()
        self.distribution = self.build_distrib()
        self.states = []
        self.backward_messages = []
        self.transition_model = self.build_transition_model()
        self.color_matrices = self.build_color_matrices()

    def read_file(self):
        lines = []
        f = open(self.file_name, "r")
        for line in f:
            line = line.strip()
            # ignore blank limes
            if len(line) == 0:
                pass
            elif line[0] == "\\":
                parms = line.split()
                x = int(parms[1])
                y = int(parms[2])
            else:
                lines.append(line)
        f.close()
        return lines

    def build_maze(self):
        maze = []
        for x in range(self.width):
            col = []
            for y in range(self.height):
                col.append(self.lines[y][x])
            maze.append(col)
        return maze

    def count_floors(self):
        count = 0
        for x in range(self.width):
            for y in range(self.height):
                if not self.is_wall(x, y):
                    count += 1
        return count

    def index(self, x, y):
        return (x * self.height) + y

    def build_distrib(self):
        distrib = []
        for x in range(self.width):
            for y in range(self.height):
                if not self.is_wall(x, y):
                    distrib.append(1/self.floor_count)
                    # self.update_evidence(x, y)
                else:
                    distrib.append(0)
        return distrib

    def build_transition_model(self):
        trans_model = [[0 for i in range(len(self.distribution))] for j in range(len(self.distribution))]

        for x in range(self.width):
            for y in range(self.height):
                if self.is_wall(x, y):
                    continue
                for neighbor in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if self.is_wall(x + neighbor[0], y + neighbor[1]):
                        trans_model[self.index(x, y)][self.index(x, y)] += 1 / 4
                    else:
                        trans_model[self.index(x + neighbor[0], y + neighbor[1])][self.index(x, y)] += 1/4
        return trans_model

    def build_color_matrices(self):
        color_matrices = dict()
        for color in self.colors:

            color_matrix = [0 for i in range(len(self.distribution))]
            # color_matrix = [[0 for i in range(len(self.distribution))] for j in range(len(self.distribution))]

            for x in range(self.width):
                for y in range(self.height):
                    if self.is_wall(x, y):
                        continue
                    # color_matrix[self.index(x, y)][self.index(x, y)] = self.sensor_accuracy \
                    #     if self.maze[x][y] == color else (1 - self.sensor_accuracy)/3
                    color_matrix[self.index(x, y)] = self.sensor_accuracy \
                        if self.maze[x][y] == color else (1 - self.sensor_accuracy) / 3
            color_matrices[color] = color_matrix

        return color_matrices

    def forward(self, is_adhoc=False):
        self.states.append(self.distribution)
        for i in range(0, len(self.color_sequence)):
            self.states.append(np.dot(self.transition_model, self.states[i]))
            if is_adhoc:
                self.filter_adhoc(self.color_sequence[i], i + 1)
            else:
                self.filter_mm(self.color_sequence[i], i + 1)

    def backward(self):
        # self.backward_messages.append([[1 for i in range(len(self.distribution))] for j in range(len(self.distribution))])
        self.backward_messages.append([1 for i in range(len(self.distribution))])
        for k in range(len(self.color_sequence)):
            color = self.color_sequence[-k - 1]
            self.backward_messages.append(np.multiply(self.color_matrices[color], self.backward_messages[k]))

    def forward_backward(self, is_adhoc=False):
        self.forward(is_adhoc)
        self.backward()
        for i in range(len(self.color_sequence)):
            back = np.dot(self.transition_model, self.backward_messages[-i - 1])
            self.states[i + 1] = np.multiply(back, self.states[i + 1])
            self.normalize_distrib(sum(self.states[i + 1]), i + 1)

    # returns a sequence of estimated robot's location with either Viterbi algorithm or with brute algorithm
    # depending on what input the method gets. Default algorithm is Viterbi.
    def most_likely_sequence(self, is_viterbi=True):
        if is_viterbi:
            return self.viterbi_search()
        else:
            max_score = 0
            max_seq = []
            seq_n_value = dict()

            for i in range(len(self.states[1])):
                x = i // self.height
                y = i % self.height
                self.brute_search(1, self.index(x, y), [self.index(x, y)], 0, seq_n_value)

            for seq in seq_n_value.keys():
                score = 0
                score = seq_n_value[seq]
                if score > max_score:
                    max_seq = seq
                    max_score = score

            return max_seq

    # Brutely compute every possible sequence
    def brute_search(self, index, pos, seq, cum_score, seq_n_value):
        if index == len(self.states) - 1:
            seq_n_value[tuple(seq)] = cum_score + self.states[index][pos]
            return

        for neighbor in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x = pos // self.height
            y = pos % self.height
            score = cum_score + self.states[index][pos]

            if self.is_wall(x + neighbor[0], y + neighbor[1]):
                self.brute_search(index + 1, pos, seq + [pos], score, seq_n_value)
            else:
                x += neighbor[0]
                y += neighbor[1]
                self.brute_search(index + 1, self.index(x, y), seq + [self.index(x, y)],
                                  score, seq_n_value)

    # Start from the end, take a step backward at a time, search for the neighboring cell with the highest
    # probability
    def viterbi_search(self):
        max_seq = []
        cur_loc = np.argmax(self.states[-1])
        max_seq.append(cur_loc)
        for t in range(2, len(self.states)):
            neighbors = self.get_neighbors(cur_loc)
            best_neighbor = 0
            best_score = 0
            for neighbor in neighbors:
                if self.states[-t][neighbor] > best_score:
                    best_neighbor = neighbor
                    best_score = self.states[-t][neighbor]
            cur_loc = best_neighbor
            max_seq.append(cur_loc)
        max_seq.reverse()
        return max_seq

    def get_neighbors(self, index):
        neighbors = []
        x = index // self.height
        y = index % self.height
        for move in [1, -1]:
            horizontal = self.index(x + move, y) if not self.is_wall(x + move, y) else index
            vertical = self.index(x, y + move) if not self.is_wall(x, y + move) else index
            neighbors.append(horizontal)
            neighbors.append(vertical)
        return neighbors

    def filter_adhoc(self, color, state_index):
        count = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.maze[x][y] == color:
                    self.states[state_index][self.index(x, y)] *= self.sensor_accuracy
                else:
                    self.states[state_index][self.index(x, y)] *= (1 - self.sensor_accuracy)/3
                count += self.states[state_index][self.index(x, y)]
        self.normalize_distrib(count, state_index)

    def filter_mm(self, color, state_index):
        self.states[state_index] = np.multiply(self.color_matrices[color], self.states[state_index])
        self.normalize_distrib(sum(self.states[state_index]), state_index)

    def normalize_distrib(self, count, state_index):
        self.states[state_index] /= count

    def is_wall(self, x, y):
        if 0 > y or self.height <= y or 0 > x or self.width <= x:
            return True
        if self.maze[x][y] == '#':
            return True
        return False

    def find_robotlocs(self):
        if self.is_wall(self.initial_loc[0], self.height - self.initial_loc[1] - 1):
            print("initial location not valid: please enter a valid location")
            return []

        robotlocs = []
        # cur_loc = self.initial_loc
        cur_loc = (self.initial_loc[0], self.height - self.initial_loc[1] - 1)
        robotlocs.append(cur_loc)
        for move in self.move_seq:
            if move == 'E':
                cur_loc = (cur_loc[0] + 1, cur_loc[1]) if not self.is_wall(cur_loc[0] + 1, cur_loc[1]) else cur_loc
            elif move == 'W':
                cur_loc = (cur_loc[0] - 1, cur_loc[1]) if not self.is_wall(cur_loc[0] - 1, cur_loc[1]) else cur_loc
            elif move == 'S':
                cur_loc = (cur_loc[0], cur_loc[1] + 1) if not self.is_wall(cur_loc[0], cur_loc[1] + 1) else cur_loc
            elif move == 'N':
                cur_loc = (cur_loc[0], cur_loc[1] - 1) if not self.is_wall(cur_loc[0], cur_loc[1] - 1) else cur_loc
            robotlocs.append(cur_loc)

        return robotlocs

    def get_color_seq(self):
        color_seq = []
        for robotloc in self.robotlocs:
            color = ''
            color_list = self.colors.copy()
            sensor_read = random.uniform(0, 1)
            if sensor_read < self.sensor_accuracy:
                color = self.maze[robotloc[0]][robotloc[1]]
                color_list.remove(color)
            else:
                color = random.choice(color_list)

            color_seq.append(color)
        return color_seq

    # randomly simulate a robot movement for n steps.
    def simulate(self, count):
        robotloc = tuple()

        # get initial point within the maze
        while True:
            rand_x = random.randint(0, self.width - 1)
            rand_y = random.randint(0, self.height - 1)
            if not self.is_wall(rand_x, self.height - rand_y - 1):
                robotloc = (rand_x, rand_y)
                break

        self.initial_loc = robotloc

        random.seed(107)
        move_seq = []
        for i in range(count):
            move = random.choice(['E', 'W', 'S', 'N'])
            move_seq.append(move)

        self.move_seq = move_seq
        self.robotlocs = self.find_robotlocs()
        self.color_sequence = self.get_color_seq()
        self.forward_backward()
        print("simulating robot movement")

    def str_matrix(self):
        max_seq = self.most_likely_sequence(is_viterbi=True) if self.get_seq else None
        separator = "-"
        for i in range(self.width * 12):
            separator += '-'
        s = "Bold yellow letters indicate robot's real location and * indicates robot's estimated location"
        # count = 0
        for i in range(len(self.states)):
            s += "\nat " + str(i)
            if len(self.robotlocs) >= i > 0:
                s += " : robot moved " + self.move_seq[i - 2] if i > 1 else ""
                s += " : robot is at " + "(" + str(self.robotlocs[i - 1][0]) + ", " + \
                     str(self.height - self.robotlocs[i - 1][1] - 1) + ")" + " and its color sensor reads " \
                     + self.color_sequence[i - 1]
            elif i > 0:
                s += " : user's given color is " + self.color_sequence[i-1]
            s += '\n' + separator + '\n'
            for y in range(self.height):
                s += "|"
                for x in range(self.width):
                    # count += state[self.index(x, y)]
                    if len(self.robotlocs) >= i > 0 and self.robotlocs[i - 1] == (x, y):
                        s += '\033[1m\033[93m '
                    else:
                        s += ' '
                    if self.get_seq and i > 0 and max_seq[i - 1] == self.index(x, y):
                        s += str('%5.4f' % self.states[i][self.index(x, y)]) + "[" + self.maze[x][y] + "]" + '*|\033[0m'
                    else:
                        s += str('%5.4f' % self.states[i][self.index(x, y)]) + "[" + self.maze[x][y] + "]" + ' |\033[0m'

                s += '\n' + separator + '\n'
        # print(count)
        return s


if __name__ == '__main__':
    start = time.time()
    test = HMM("test.maz", (2, 0), ['N', 'W', 'N', 'N'])
    # test.forward()
    # test.forward_backward()
    test.simulate(10)
    print(test.str_matrix())
    end = time.time()
    print("Time elapsed : " + str(end - start))

