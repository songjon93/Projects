import planarsim
import random
import math
from Space import Space


class CarRobot:
    def __init__(self, space: Space, width=5, height=10):
        self.space = space
        self.width = width
        self.height = height
        self.generated_random = set()

    # Return a random configuration in c-space.
    def random_choice(self):
        repeat = True
        config = None

        while repeat:
            ran_x = random.uniform(-1, 1) * self.space.width
            ran_y = random.uniform(-1, 1) * self.space.height
            ran_theta = random.uniform(0, 2 * math.pi)
            config = [ran_x, ran_y, ran_theta]

            if tuple(config) not in self.generated_random:
                self.generated_random.add(tuple(config))
                repeat = False

        return config
