### Robot Movement
In this lab, I have designed motion planners for two systems: a planar robot arm, and a steered car. Two different motion planning algorithms will utilized for the two robots; one being Probabilistic Road Mapping (PRM) and the other being Rapidly Exploring Random Tree.

**Extra Credits** are documented at the bottom.
#### Design Overview / Implementation
##### Planar Robot Arm
1. Space:
    ```
    def __init__(self, width, height,  obstacle_size=30, n_obstacles=5, default=True):

    A cartesian space of size (2 width * 2 height) with square obstacles of specified sizes.

    The robot arm will be stationed in this space, and our motion planning algorithm will have to find a collision free path from the start state to the end state.
    ```
2. Robot:
    ```
    def __init__(self, lengths, width=5):

    Our arm robot will be generated with the user inputted arm lengths and widths.

    Our robot object will be used to generate random configuration of the robot and to translate a list of angle configurations into cartesian coordinates.

    And the object will hold a set of generated random configurations to prevent any identical random generation.

    ** widths will only be utilized in our extra credit version of our program that is capable of sampling rectangular links.
    ```
3. Probabilistic Road Mapping (PRM):
    ```
    PRM will generate a roadmap of collision-free paths. In determining whether a path from one vertex to another causes collision or not, we will implement a sampling method that will divide the robot motion from one configuration to another in certain time steps (provided by the user), and see if any of the arm coincides with an obstacle.
    ```
4. Illustrate:
    ```
    This file will be used to animate the robot's motion from a specified start state to the end state.

    I have provided a demo video of the arm robot motion in the submission.

    For a more advanced demonstration with each arm being depicted as a rectangle, check MotionPlanning_EC.
    ```
##### Steered Car Robot
1. Space:
    ```
    Our steered car robot shares the same cartesian space with our arm robot. Hence, we will be using the same "space.py" file.
    ```
2. Robot:
    ```
    def __init__(self, space: Space, width=5, height=10):

    Our robot object will be used to generate random configuration (x, y, θ).

    And the object will hold a set of generated random configurations to prevent any repetition.
    ```
3. Rapidly Exploring Random Trees (RRT):
    ```
    RRT will also generate a roadmap of collision-free paths. Each vertex within the graph will hold a pointer to its parent vertex so that when we reach our goal, we have the collision-free path from the start to the end.

    At each iteration, we will be adding 6 new vertices to the graph. Hence, the more iteration there are the more dense our roadmap will be.

    In order to detect collisions, we will be using the identical sampling method from the above.
    ```
4. Illustrate:
    ```
    We will be creating a robot object, a space object, and a RRT object with inputs of our choice. And we will be animating the automated robot steering its way toward the goal. Moreover, our illustration will include a web of the robot's possible paths, which is in essence our computed roadmap.

    I have provided a demo video of the arm robot motion in the submission.

    Note that a robot is depicted as a circle with a radius of 2 despite it being a point in our algorithm for a clearer portrayal. And therefore, it may sometimes seem as if it is penetrating through the edge of an obstacle by a little.

    For a more advanced demonstration with a robot being depicted as a rectangle, check MotionPlanning_EC.
    ```
#### Codes Revisited

##### PRM
###### def build_roadmap():
```
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
        # nearby_n = self.ann_k_neighbors(neighbors, key)
        for neighbor in nearby_n:
            if key in road_map[neighbor] or not self.collision_btw(key, neighbor):
                road_map[key].add(neighbor)
            else:
                print("collision detected")

    print("roadmapping complete")
    return road_map
```
In the beginning of the method, we append to the graph our start and the end state. Then, we randomly select a configuration, look through its _k_ closest neighbors. And we sample robot's motion from each neighbor to the selected configuration, check for collision, and draw edges between them only if there were no collision. And we repeat the procedure for a given number of iterations.

###### def get_k_neighbors(neighbor, goal)
```
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
```
The function loops through the entire vertices of the graph, and sorts the vertices according to their distances from the `goal` (not our end state, but the randomly generated robot configuration that we are trying to append to our graph). And we will be returning the first _k_ vertices within the sorted list.

However, this function is highly inefficient because it loops through and sorts the entire vertices in the graph, which is at least `O(n * log(n))`. And this function will be called _n_ times in building the road map, and we end up with `O(n^2 * log(n))` time complexity.

In order to accelerate the process, I have implemented ANN algorithm as an extension, which can be seen at the bottom of this document.

###### def is_collision(config):
```
def is_collision(self, config):
    positions = self.robot.config_positions(config)
    for obstacle in self.space.obstacles:
        if LineString(positions).intersects(Polygon(obstacle)):
            return True
    return False
```
The function uses _Shapely_ library to check if our robot arm intersects with any of the obstacle within the space.


###### def collision_btw(c1, c2):
```
def collision_btw(self, c1, c2):
    for i in range(self.time_step):
        config = []

        for joint in range(len(c1)):
            sample = self.min_angular_distance(c1[joint], c2[joint]) / self.time_step

            computed = self.normalize_angle(c1[joint] + ((i + 1) * sample))

            config.append(computed)

        if self.is_collision(config): return True
```
This method determines if the robot arm ever collides to any of the obstacle in the space as it moves from _config #1_ to _config #2_. In order to do so, I decided to sample _n_ (specified as self.time_step) Cartesian coordinates of the robot from _config #1_ to _config #2_. If we encounter a sample in which the robot's arm coincides (collides) with an obstacle, we will return True.

###### etc.
**min_angular_dsitance** is used to determine the shortest angular distance from _a1_ to _a2_. It returns a negative value if a clockwise movement is the shortest angular distance and a positive value if the otherwise.

**normalize_angle** is used to normalize the angle so that it always fits under the range between 0 and 2 pi.

**smooth** method is used for animating the robot motion. In order to increase the number of frames, the method samples more Cartesian coordinates of the robot. Using this method significantly enhances the quality of the animation.

**find_path** method utilizes _BFS_ algorithm to search for the shortest path from the specified start state to the end stated.

##### RRT
###### def explore()
```
def explore(self):
    graph = dict()
    graph[tuple(self.start)] = None
    counter = 0

    while counter < self.iteration:
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
                        duration -= self.timestep
                        found = True

                else:
                    found = True

            if prev_config not in graph.keys():
                graph[prev_config] = (i, duration, neighbor)

    self.end = self.get_nearest_vertex(self.end, graph)

    return graph

```
This method essentially is the blueprint of our RRT algorithm. At every iteration, we will pick a random configuration of a robot, and build vertices and edges based on this random configuration.

We will be sampling six basic movements of the robot: 1) moving forward, 2) moving backward, 3) moving forward and clockwise, 4) moving forward and counter-clockwise, 5) moving backward and clockwise, and 6) moving backward and counter_clockwise. And we will proceed until we've reached a point where we collide into an obstacle, or until we have gotten as close as possible to our inputted random configuration. Then, we will be appending this vertex to our graph along with the robot control that got us there so that we can later emulate the robot motion using the graph.

###### def is_collision(config)
```
def is_collision(self, config):
    if config[0] > self.space.width or config[0] < -self.space.width or \
                    config[1] > self.space.height or config[1] < -self.space.height:
        return True

    for obstacle in self.space.obstacles:
        if Polygon(obstacle).intersects(Point(config[0], config[1])):
            return True

    return False
```
This method checks if the robot's coordinates are where the obstacle is stationed at. I use `intersects` function from _Shapely_ library instead of `contains` function because `contains` function will not detect the cases where the robot lies at the edge of the obstacle. I would suppose that one could use `contains` function if one were to call such states legal but I decided to call them illegal states.

##### def draw_map(graph : dict(), epsilon):
```
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
```
This method is used for illustration purpose. It is to depict the trajectory of the robot's possible legal motions computed previously in our `explore` method. In order to prevent the trajectory from having a choppy look, I use sampling method to have a smoother and more accurate portrayal of the trajectories.

One thing to take note is that if the smaller the epsilon value is the smoother trajectories will be. However, this will cause the program to slow down because it intrinsically means more loops and more computations.

##### def get_nearest_vertex(vertex, graph : dict()):
```
def get_nearest_vertex(self, vertex, graph:dict):
    min_dist = float("inf")
    min_neighbor = None

    for neighbor in graph.keys():
        dist = self.compute_distance(vertex, neighbor)

        if dist < min_dist:
            min_dist = dist
            min_neighbor = neighbor

    return min_neighbor
```
Given a random configuration within the c-space, this method will loop through the entire vertices within the computed graph, and return the vertex with the shortest euclidean distance from the configuration.

This method will be used at every iteration of our RRT algorithm. We will be sampling robot's motion from the returned vertex.

Moreover, we will call this method one more time at the end of the RRT algorithm to replace our `self.end_state` with the vertex within our graph that is the closest from our desired end state because our RRT search comes to an end not when we find our path to the goal but when we have completed the number of iteration specified when initializing the RRT object.

##### etc.
Our **backtrack** method will build a path from the _end_ vertex to the _start_ vertex. As mentioned earlier, every vertex within the graph will hold a pointer to its parent vertex, and, thus, we can easily find the path by looping from the end to the start and reversing the list.

Our **normalize_pos** method in our illustration file normalizes our coordinates so that (0, 0) represents the center of the canvas not the left-top corner.

Our **do_scale** method scales the size of the robot, trajectories, obstacles, and the canvas. This is used in our illustration file to illustrate the trajectory of the robot motion in a more detailed manner.

#### Topic Discussion
##### PRM
PRM is a form of sampling-based planning. The basic idea behind the algorithm is to select a random configuration from the c-space and try to draw edges between the selected configuration and its _k_ nearest neighbors.

In PRM, we intrinsically are trying to portray the c-space through trial and error phases. Since the road map shows all legal paths among vertices, we can find a collision-free paths from the start state to the goal state of our choice.

###### Discussion Questions and Answers
1. What affect does the number of neighbors in get_k_neighbors have in the general efficiency of our PRM algorithm?

      _Essentially the more neighbors we look at, the denser our roadmap will be. However, at the same time, the time complexity of our program will increase at an exponential rate._

      _That is why we limit the number of neighbors we try connecting the randomly selected configuration to. However, it is very important to note that if the number of neighbor is too small, we could face possible risks of having a disjoint graph and not being able to find a path from one vertex to another._

2. What is a possible loophole in sampling method?

    _If we don't sample enough, we might not catch a collision between the obstacle and the robot. The further the robot's arm is from the origin, the more likely it is for this algorithm to skip a collision. And that is why we have to sample a significant amount; however, the more we sample the slower and heavier our program will be. Hence, it is very important to alter the sampling size in correspondence to the total length of robot._

3. What is a dense road map?

    _A dense road map would give us an adequate portrayal of the robot's configuration space. In other word, if our road map contains as its vertices a significant portion of obstacle-less space, we would be able to refer to our road map as a dense road map._

##### RRT
The basic idea behind RRT algorithm is as follows:
1. select a random configuration from the c-space
2. try drawing an edge from the most nearby vertex to the selected configuration.
3. If there occurs a collision in between, draw a vertex right before the collision occurs and draw an edge  to the newly drawn vertex.
4. Repeat until our roadmap is dense enough.

In our implementation of RRT, we are trying to find a path from the specified start point to the end point. Therefore, our roadmap will be a graph of vertices, where each vertex will be holding a pointer to its parent vertex, one of the six controls the robot was operating under, and the duration of the movement. With these contents, it was rather easy at the end to replicate the robot's movement and animate robot's motion from the start point to the end.

###### Discussion Questions and Answers

1. A robot's position is represented with a 3 tuple of real numbers (x, y, θ), and hence, it would take up to infinite number of iterations to reach the goal. What is a reasonable resolution to this problem?

    _A possible resolution to this problem would be to set a goal_proximity value, and claim that you have reached the goal when RRT has found a vertex for which the distance from the vertex to the goal is smaller than the proximity value. And once the search is over, you'd replace the _self.end_ with that vertex. For my implementation, I set my default to 5, but it can be altered by the user through feeding the object with a different value._

2. What is a possible loophole in sampling method?

    _Essentially the same loophole from PRM exists in RRT as well. It is possible for the robot to skip an obstacle if the sampling size is not large enough._

3. Is RRT an appropriate method in finding the shortest path to the goal?

    _No, RRT only computes a legal path from _a_ to _b_, and does not guarantee the shortest path. Our roadmap is a tree, and therefore, in order to move from a leaf node to another, you would have to climb up to a common parent node, and climb all the way again._
#### Extra Credits:
1) **Arm Robot with a polygonal representation**

    Instead of representing each arm of the robot with a line, I decided to represent it with a rectangle. In order to do so, I had to implement a rotation equation, where I compute the coordinates of the four edges of the rectangle given an angle and the point of rotation.

    Moreover, when checking for collisions, instead of checking for intersection between a polygon and a line string, the program would be checking for intersection between two polygons.

    Below is how I compute the coordinates of the 4 edges of the rectangle for each arm.
    ```
    i = 0
    accum = 0
    for angle in config:
        accum += angle
        a = (-(-self.robot.width) * math.sin(accum) + positions[i][0],
             (-self.robot.width) * math.cos(accum) + positions[i][1])
        b = (-self.robot.width * math.sin(accum) + positions[i][0],
             self.robot.width * math.cos(accum) + positions[i][1])
        c = (
            (self.robot.lengths[i]) * math.cos(accum) - self.robot.width * math.sin(accum) + positions[i][0],
            (self.robot.lengths[i]) * math.sin(accum) + self.robot.width * math.cos(accum) + positions[i][1])
        d = (self.robot.lengths[i] * math.cos(accum) - (-self.robot.width * math.sin(accum)) + positions[i][0],
             self.robot.lengths[i] * math.sin(accum) + (-self.robot.width * math.cos(accum)) + positions[i][1])
        i += 1
    ```

    A demonstration video can be found within the MotionPlanning_EC folder. Moreover, the user can run the actual program by running illustrate_PRM.py file.

2) **Car Robot with a polygonal representation**

    Instead of representing the car with a single point, I gave it a rectangular representation. This also uses a rotation equation introduced above

    In fact, representing the robot with a rectangle made the program run faster with a more accurate result because there is a less likely chance that the collision check method will skip the obstacle if the robot has a figurative size even with a smaller sampling size.

    Below is how I compute the coordinates of the car robot:
    ```
    cur_config = config_from_transform(transform)

    a = (self.robot.width * math.sin(cur_config[2]) + cur_config[0],
         (-self.robot.width) * math.cos(cur_config[2]) + cur_config[1])
    b = (-self.robot.width * math.sin(cur_config[2]) + cur_config[0],
         self.robot.width * math.cos(cur_config[2]) + cur_config[1])
    c = (self.robot.height * math.cos(cur_config[2]) - self.robot.width * math.sin(cur_config[2]) + cur_config[0],
         self.robot.height * math.sin(cur_config[2]) + self.robot.width * math.cos(cur_config[2]) + cur_config[1])
    d = (self.robot.height * math.cos(cur_config[2]) + self.robot.width * math.sin(cur_config[2]) + cur_config[0],
         self.robot.height * math.sin(cur_config[2]) - self.robot.width * math.cos(cur_config[2]) + cur_config[1])
    ```

    A demonstration video can be found within the MotionPlanning_EC folder. Moreover, the user can run the actual program by running illustrate_RRT.py file.

3) **ANN algorithms for finding k neighbors**
    As previously discussed, it is inefficient to sort the entire vertices within the graph for retrieving _k_ nearest neighbors. Therefore, I decided to implement an ANN algorithm for a more efficient search.

    Because computing euclidean distances of the configuration vectors would give us a wrong k neighbors (since it only computes an absolute distance and doesn't take into account that there are two possible distances from config_1 to config_2: clockwise and counterclockwise movements), I had to modify the codes so that the vectors that are stored in the annoy tree are not vectors of radian values but vectors of Cartesian coordinates. The outcome was quite satisfactory, but the search time was not curtailed to a drastic amount as I expected. However, the testing was executed with only 1000 vertices. It is expected that there will be a bigger improvement with more vertices.

    `def ann_k_neighbors(self, neighbors, config):` can be found in PRM.py in MotionPlanning_EC.

4) **Paper Reviewed**

    **The Gaussian Sampling Strategy for Probabilistic Roadmap Planners**
    _by Valerie Boor, Mark H. Overmars, A. Frank van der Stappen_

    This paper suggests a new sampling method _Gaussian sampler_ that gives a better coverage with a smaller number of samples. Gaussian sampler uses blurring technique like in done in  photographic processing.

    Gaussian sampler especially shows a major improvement in selecting a random configuration in a free configuration space (where there is no obstacle). And that is why Gaussian sampler cuts a fine figure in spaces that are heavily occupied by obstacles. What is even more amazing is that Gaussian sample does not require any complicated geometric computation like other methods, but a simple intersection test.

    The test results showed that Gaussian sampling ran 60 times faster in comparison to random sampling method.

    However, the author suggests that there remain issues to be overcome. First, the author has not been able to figure the exact role standard deviation plays in Gaussian sampling. And second, Gaussian sampling has not been tested for high-dimensional workspaces. Regardless, it seems definite that Gaussian sampling offers a new insight to conventional Probabilistic Road Mapping.
