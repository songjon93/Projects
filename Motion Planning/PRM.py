from ArmRobot import PlanarRobot
from Space import Space
from shapely.geometry import Polygon, LineString
import math
import random
from annoy import AnnoyIndex


class PRM:
    def __init__(self, space : Space, robot : PlanarRobot, iteration, k, sample_size=50, start=None, end=None, ):
        self.space = space
        self.robot = robot
        self.start = self.select_point(start)
        self.end = self.select_point(end)
        self.iteration = iteration
        self.k = k
        self.sample_size = sample_size

    # Return user input if there is one in a correct format
    # If not, return a randomly generated start / end state
    def select_point(self, config):
        if config is None:
            print("No start / end state detected, generating random start / end state")
            return self.robot.random_choice()
        elif len(config) != len(self.robot.lengths):
            print("Invalid start / end state, generating random start / end state.")
            return self.robot.random_choice()
        else:
            return config

    # Generate a roadmap of robot's configuration. The vertices with edges in between are those that can be
    # traveled from and to collision free.
    def build_road_map(self):
        road_map = dict()
        road_map[tuple(self.start)] = set()
        road_map[tuple(self.end)] = set()

        for i in range(self.iteration):
            config = tuple(self.robot.random_choice())

            if self.is_collision(config):
                continue

            road_map[config] = set()

        for key in road_map.keys():
            neighbors = set(road_map.keys())
            neighbors.remove(key)

            nearby_n = self.get_k_neighbors(neighbors, key)
            for neighbor in nearby_n:
                if key in road_map[neighbor] or not self.collision_btw(key, neighbor):
                    road_map[key].add(neighbor)
                else:
                    print("collision detected")

        print("roadmapping complete")
        return road_map

    # Using the generated roadmap, find a path using BFS from the start state to the end state.
    def find_path(self):
        prm = self.build_road_map()
        visited = set()
        path_exists = False
        queue = [tuple(self.start)]
        tracker = dict()

        while len(queue) > 0:
            print(len(queue))
            cur = queue.pop(0)
            if cur in visited:
                continue
            visited.add(cur)
            if cur == tuple(self.end):
                path_exists = True
                print("path found!")
                break
            for child in prm[cur]:
                if tuple(child) not in visited:
                    tracker[tuple(child)] = cur
                    queue.append(tuple(child))

        path = []

        if path_exists:
            path = backtrack(tracker, tuple(self.start), tuple(self.end))

        path.reverse()

        smoothed = []
        for i in range(len(path) - 1):
            smoothed.append(path[i])
            self.smoothing(path[i], path[i + 1], smoothed)
        return smoothed

    # Compute euclidean distance between for all vertices and return k nearest neighbors.
    def get_k_neighbors(self, neighbors, goal):
        n = []

        for neighbor in neighbors:
            dist = self.compute_euc_distance(goal, neighbor)
            n.append(tuple((neighbor, dist)))

        n = sorted(n, key=lambda x:x[1])
        ret = []
        for i in range(self.k):
            ret.append(n[i][0])
        return ret

    # Compute angular distance between the two. There exist two : clockwise and counterclockwise.
    # Always return the smaller of the two.
    def compute_angular_distance(self, a1, a2):
        clockwise = abs(a1 - a2)
        counter = 2 * math.pi - clockwise
        return min(clockwise, counter)

    # Compute angular distances of all the joints and find the euclidean distances.
    # This function will be used to find k nearest neighbors.
    def compute_euc_distance(self, c1, c2):
        dist = 0
        for i in range(len(c1)):
            dist += self.compute_angular_distance(c1[i], c2[i])**2
        return math.sqrt(dist)

    # Check if the robot's arms are coinciding with any of the obstacles in the space.
    def is_collision(self, config):
        positions = self.robot.config_positions(config)
        for obstacle in self.space.obstacles:
            if LineString(positions).intersects(Polygon(obstacle)):
                return True
        return False

    # Sample robot's movement from c1 to c2, and check for collisions.
    # The larger the sample size, the more accuarate the result will be, but this also means longer run-time.
    def collision_btw(self, c1, c2):
        for i in range(self.sample_size):
            config = []

            for joint in range(len(c1)):
                sample = self.min_angular_distance(c1[joint], c2[joint]) / self.sample_size

                computed = self.normalize_angle(c1[joint] + ((i + 1) * sample))

                config.append(computed)

            if self.is_collision(config): return True

        return False

    def min_angular_distance(self, c1, c2):
        counter = c2 - c1 if c2 > c1 else 2 * math.pi - abs(c2 - c1)
        clock = 2 * math.pi - counter
        ret = -clock if clock < counter else counter

        return ret

    # Normalize the inputted radian value to a range from 0 to 2 pi
    def normalize_angle(self, angle):
        if angle < 0: ret = angle + 2 * math.pi
        if angle > 2 * math.pi: ret = angle - 2 * math.pi

        return angle

    # Used for illustration. Sample robot motions for a smooth animation.
    # Caution: if the sample size for collision_btw was too small, you may see robot's arm moving through an obstacle.
    def smoothing(self, c1, c2, smoothed):
        for i in range(self.sample_size):
            config = []
            for joint in range(len(c1)):
                counter = c2[joint] - c1[joint] if c2[joint] > c1[joint] else 2 * math.pi - abs(c2[joint] - c1[joint])
                clock = 2 * math.pi - counter
                sample = float
                if clock < counter:
                    sample = -clock / self.sample_size
                else:
                    sample = counter / self.sample_size

                computed = c1[joint] + ((i + 1) * sample)
                if computed < 0: computed += 2 * math.pi
                if computed > 2 * math.pi: computed -= 2 * math.pi

                config.append(computed)

            if self.is_collision(config): print("?")
            smoothed.append(tuple(config))

# Given a tracker in which each vertex holds a pointer to its parent vertex, backtrack from the end to the start
# for a list of path.
def backtrack(tracker, start, end):
    path = [end]
    vertex = end
    print(start)
    print(end)
    while vertex != start:
        print(vertex)
        vertex = tracker[vertex]
        path.append(vertex)
    return path
