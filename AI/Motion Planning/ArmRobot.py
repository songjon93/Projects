import math
import random


class PlanarRobot:
    def __init__(self, lengths, width=5):
        self.lengths = lengths
        self.width = width
        self.generated_rand = set()

    # Translate configuration coordinates into Cartesian coordinates.
    def config_positions(self, config):
        vertices = [(0, 0)]
        cum_angle = 0
        prev_x = 0
        prev_y = 0
        for i in range(len(config)):
            x = self.lengths[i] * math.cos(config[i] + cum_angle) + prev_x
            y = self.lengths[i] * math.sin(config[i] + cum_angle) + prev_y
            prev_x = x
            prev_y = y
            cum_angle += config[i]
            vertices.append((x, y))
        return vertices

    # Return a random configuration from the c-space.
    def random_choice(self):
        random_config = None
        repeat = True

        while repeat:
            random_config = []
            for i in range(len(self.lengths)):
                ran = random.uniform(0, 2 * math.pi)
                random_config.append(ran)
            if tuple(random_config) not in self.generated_rand:
                self.generated_rand.add(tuple(random_config))
                repeat = False

        return random_config
