from PRM import PRM
from ArmRobot import PlanarRobot
from Space import Space
from shapely.geometry import Polygon
import random
import cs1lib
import time
import math

if __name__ == '__main__':
    # Define your space with width, height, the number of obstacles, and their size.
    space = Space(300, 300, obstacle_size=30, n_obstacles=20)
    # Define your robot with a list of arm lengths.
    # The size of the list would signify the number of joints the robot will have.
    robot = PlanarRobot([space.width//3, space.width//3, space.width//3, space.width//3], 8)
    # Specify your start state
    start = [3 * math.pi / 2, 0, 0, 0]
    # Specify your end state
    end = [0, 0, math.pi/2, 0]
    # Define your PRM with the number of iterations and the number of neighbors you want to look at.
    test = PRM(space, robot, 1000, 10, start=start, end=end)
    res = test.find_path()
    index = 0

    # Draw an illustration of the robot at each index, increment the index by 1 at every iteration.
    # Once hit the end, return to 0.
    def draw_illustration():
        cs1lib.set_clear_color(1, 1, 1)
        cs1lib.disable_stroke()
        cs1lib.clear()
        global res, index
        config = res[index]
        if index == 0: time.sleep(3)
        index = (index + 1) % len(res)
        positions = robot.config_positions(config)

        for obstacle in space.obstacles:
            cs1lib.enable_fill()
            cs1lib.set_fill_color(0, 0, 0)
            cs1lib.draw_rectangle(obstacle[3][0] + space.width, -obstacle[3][1] + space.height,
                                  space.obstacle_size, space.obstacle_size)

        cs1lib.set_fill_color(.5, .5, .5)
        angle = 0
        pos = normalize_pos(positions)
        for i in range(len(positions) - 1):
            cs1lib.enable_stroke()
            cs1lib.draw_line(pos[i][0], pos[i][1], pos[i + 1][0], pos[i + 1][1])

        if index == 0:
            draw_game_clear()

    # When the goal state has been reached, a game clear sign will pop up.
    def draw_game_clear():
        cs1lib.set_font_bold()
        cs1lib.set_font_size(30)
        x = cs1lib.get_text_width("Game Clear")
        cs1lib.draw_text("Game Clear", space.width - x/2, space.height - cs1lib.get_text_height()/2)

    # Normalize the coordinates the robot and the obstacles so that (0, 0) is the center of the canvas.
    # and so that the smaller y signfies a lower point at canvas.
    def normalize_pos(positions):
        for i in range(len(positions)):
            positions[i] = (positions[i][0] + space.width, -positions[i][1] + space.height)
        return positions

    if len(res) == 0:
        print("solution not found")
    else:
        cs1lib.start_graphics(draw_func=draw_illustration, width=space.width * 2, height=space.height * 2, framerate=test.sample_size / 2)
