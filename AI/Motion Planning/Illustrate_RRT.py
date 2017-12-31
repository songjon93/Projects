from RRT import RRT
from ArmRobot import PlanarRobot
from Space import Space
from shapely.geometry import Polygon, LineString
import random
import cs1lib
from cs1lib import *
import numpy as np
import math
import time

if __name__ == '__main__':
    # Define your space with width, height, the number of obstacles, and their size.
    space = Space(10, 10, obstacle_size=1, n_obstacles=100, default=False)
    # Define your robot with the width and the height (for extension only)
    robot_size = (0.25, .5)
    # Specify the start and the end state of the robot.
    start = (-space.width + 1.5 * robot_size[1], -space.height + 1.5 * robot_size[0], 0)
    end = (space.width - robot_size[1], space.height - robot_size[0], 0)
    # Design your RRT model with the number of iterations you desire
    # and how many timesteps you want to split the motions into.
    test = RRT(space, start, end, robot_size[0], robot_size[1], iteration=3000, timestep=.1)
    res = test.explore()
    rmap = test.draw_map(res, .1)
    path = test.back_track(res)
    path = test.smoothing(path)
    # Scale your coordinates so that you have a better view of the robot's trajectories and so far.
    scale = 35
    index = 0

    # Draw robot at each time index. For faster robot movement, increment the index with a larger number.
    def draw_illustration():
        cs1lib.set_clear_color(1, 1, 1)
        cs1lib.clear()
        global path, index

        config = path[index][0:2]

        index = (index + 5) % len(path)

        pos = do_scale([config[0] + space.width, space.height - config[1]])

        for obstacle in space.obstacles:
            scaled_ob = do_scale(normalize_pos(obstacle))
            disable_stroke()
            set_fill_color(.5, .5, .5)
            cs1lib.draw_rectangle(scaled_ob[3][0], scaled_ob[3][1],
                                  scale * space.obstacle_size, scale * space.obstacle_size)

        for key in rmap:
            for i in range(len(rmap[key]) - 1):
                enable_stroke()
                scaled_line = do_scale(normalize_pos(rmap[key][i:i + 2]))
                cs1lib.draw_line(scaled_line[0][0], scaled_line[0][1], scaled_line[1][0], scaled_line[1][1])

        disable_stroke()
        set_fill_color(0, 0, 0)
        cs1lib.draw_circle(pos[0], pos[1], 3)

        if index == 0:
            draw_game_clear()

    def draw_game_clear():
        cs1lib.set_font_bold()
        cs1lib.set_font_size(30)
        x = cs1lib.get_text_width("Game Clear")
        cs1lib.draw_text("Game Clear", space.width - x/2, space.height - cs1lib.get_text_height()/2)

    # Multiply the coordinates by the scale variable.
    def do_scale(positions):
        return np.multiply(positions, scale)

    # Normalize the coorindates so that (0,0) is the center of the canvas.
    # and so that the smaller y signfies a lower point at canvas.
    def normalize_pos(positions):
        new_pos = []
        for i in range(len(positions)):
            new_pos.append((positions[i][0] + space.width, -positions[i][1] + space.height))
        return new_pos

    if len(res) == 0:
        print("solution not found")
    else:
        # cs1lib.clear()
        cs1lib.start_graphics(draw_func=draw_illustration, width=space.width * 2 * scale,
                              height=space.height * 2 * scale, frames=100, framerate=60)
