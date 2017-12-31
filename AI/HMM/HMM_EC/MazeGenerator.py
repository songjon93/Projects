import random


class MazeGenerator:
    def __init__(self, width, height, file_name):
        self.width = width
        self.height = height
        self.file_name = file_name
        self.colors = ['r', 'g', 'b', 'y']

    def generate_random_maze(self):
        f = open(self.file_name, "w")
        for row in range(self.height):
            for col in range(self.width):
                f.write(random.choice(self.colors + ['#']))
            f.write('\n')
        f.close()