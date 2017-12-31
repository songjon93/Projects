from shapely.geometry import Polygon, LineString, Point
from CarRobot import CarRobot
from Space import Space
import math
import random
from planarsim import *


class RRT:
    def __init__(self, space: Space, start, end, width=5, height=10, goal_proximity=5, iteration=500, timestep=1):
        self.space = space
        self.robot = CarRobot(space, width, height)
        self.start = start
        self.end = end
        self.goal_proximity = goal_proximity
        self.iteration = iteration
        self.timestep = timestep

    # At every iteration pick a random configuration of a robot
    # and build vertices and edges based on this random configuration
    def explore(self):
        graph = dict()
        graph[tuple(self.start)] = None
        counter = 0
        reached = False

        while counter < self.iteration or not reached:
            rand = self.end if counter % 100 == 0 else self.robot.random_choice()

            counter += 1
            print(counter)
            neighbor = self.get_nearest_vertex(rand, graph)

            for i in range(len(controls_rs)):
                origin = transform_from_config(neighbor)
                transform = (origin @ transform_from_control(controls_rs[i], self.timestep))

                prev_config = config_from_transform(origin)
                found = False
                min_dist = float("inf")
                duration = 0

                while not found:
                    cur_config = config_from_transform(transform)

                    collide = self.is_collision(cur_config)

                    if not collide:
                        duration += self.timestep

                        dist = self.compute_distance(prev_config, rand)

                        if dist < min_dist:
                            min_dist = dist
                            prev_config = config_from_transform(transform)
                            transform = (transform @ transform_from_control(controls_rs[i], self.timestep))

                        else:
                            reached = True if rand == self.end and min_dist < self.goal_proximity else False
                            duration -= self.timestep
                            found = True

                    else:
                        found = True

                if prev_config not in graph.keys():
                    graph[prev_config] = (i, duration, neighbor)

        self.end = self.get_nearest_vertex(self.end, graph)

        return graph

    # Check if robot's coordinate is intersected by any of the obstacle within the space
    # + make sure the robot never escapes the space boundary.
    def is_collision(self, config):
        if config[0] > self.space.width or config[0] < -self.space.width or \
                        config[1] > self.space.height or config[1] < -self.space.height:
            return True

        for obstacle in self.space.obstacles:
            if Polygon(obstacle).intersects(Point(config[0], config[1])):
                return True

        return False

    # For depicting robot trajectory: sample robot trajectories (every edges)
    # The smaller the epsilon is, the smoother the trajectory will be.
    def draw_map(self, graph: dict(), epsilon):
        roadmap = dict()
        for key in graph.keys():
            if key == self.start: continue
            cur = transform_from_config(graph[key][2])
            control = controls_rs[graph[key][0]]
            roadmap[key] = [graph[key][2]]
            time = 0
            while time < graph[key][1]:
                cur = (cur @ transform_from_control(control, epsilon))
                config = config_from_transform(cur)
                roadmap[key].append(config[:2])
                time += epsilon
        return roadmap

    # Because the vertices in our tree holds a pointer to its parent, backtrack from the 'end' vertex
    # to the start 'vertex', which is essentially the root of the tree.
    def back_track(self, graph: dict()):
        path = [(0, 0, self.end)]
        cur = graph[tuple(self.end)]
        while cur is not None:
            path.append(cur)
            cur = graph[cur[2]]
        path.reverse()

        return path

    # For illustration / animation purpose, sample robot motions for smooth animation.
    def smoothing(self, path):
        smoothed = [path[0][2]]
        print("smoothing in process")

        for i in range(len(path) - 1):
            cur = transform_from_config(path[i][2])
            control = controls_rs[path[i][0]]
            time = 0

            while time < path[i][1]:
                cur = (cur @ transform_from_control(control, self.timestep))
                time += self.timestep
                config = config_from_transform(cur)
                smoothed.append(config)

        return smoothed

    # Given a randomly selected vertex, return a vertex in the graph that has the shortest euclidean distance from the
    # vertex.
    def get_nearest_vertex(self, vertex, graph:dict):
        min_dist = float("inf")
        min_neighbor = None

        for neighbor in graph.keys():
            dist = self.compute_distance(vertex, neighbor)

            if dist < min_dist:
                min_dist = dist
                min_neighbor = neighbor

        return min_neighbor

    # Compute a euclidean distance from a vertex to another.
    def compute_distance(self, v1, v2):
        return math.sqrt(abs(v1[0] - v2[0])**2 + abs(v1[1] - v2[1])**2)

