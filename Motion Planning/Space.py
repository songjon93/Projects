import random
from shapely.geometry import Polygon

class Space:
    def __init__(self, width, height,  obstacle_size=30, n_obstacles=5, default=True):
        self.width = width
        self.height = height
        self.obstacle_size = obstacle_size
        self.obstacles = self.generate_obstacles(width, height) if default else self.generate_random_obstacles(n_obstacles)

    # Generate default obstacles stationed at four corners of the space.
    def generate_obstacles(self, width, height):
        obstacles = []
        for x in range(-width//2 - self.obstacle_size, width, width):
            for y in range(-height//2 - self.obstacle_size, height, height):
                obstacles.append([(x, y), (x + self.obstacle_size, y), (x + self.obstacle_size, y + self.obstacle_size),
                                  (x, y + self.obstacle_size)])
        return obstacles

    # Randomly generate n obstacles of specified size. This is a very useful method in generating a maze for the robots.
    def generate_random_obstacles(self, n_obstacles):
        obstacles = []
        for i in range(n_obstacles):
            repeat = True
            while repeat:
                x = random.choice(range(-self.width + 1, self.width, 1))
                y = random.choice(range(-self.height + 1, self.height, 1))
                repeat = False if (x, y) not in obstacles else True
            obstacles.append([(x, y), (x + self.obstacle_size, y), (x + self.obstacle_size, y + self.obstacle_size),
                              (x, y + self.obstacle_size)])
        return obstacles

