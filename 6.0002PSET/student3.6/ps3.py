#
# Problem Set 3: Simulating robots
# Name: Elaheh Ahmadi
# Collaborators (discussion): N/A
# Time: 10h

import math
import random
import matplotlib

matplotlib.use("TkAgg")

import ps3_visualize
import pylab

from ps3_verify_movement3 import test_robot_movement

BIG_THETA = 359

# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """

    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """

    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        # Initializing every variable in the RectangularRoom class
        self.width = width
        self.height = height
        self.tiles = {}
        for i in range(width):
            for j in range(height):
                self.tiles[(i, j)] = dirt_amount

    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        m = math.floor(pos.get_x())
        n = math.floor(pos.get_y())
        self.tiles[(m, n)] -= capacity
        if self.tiles[(m,n)] < 0:
            self.tiles[(m,n)] = 0

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        return self.tiles[(m, n)] == 0

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        num_of_clean = 0
        # Iterates over the tiles and increase the value of num_of_clean if the dirt in that location is 0
        for i in range(self.width):
            for j in range(self.height):
                if self.tiles[(i, j)] == 0:
                    num_of_clean += 1
        return num_of_clean

    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        return 0 <= pos.get_x() < self.width and  0 <= pos.get_y() < self.height

    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return self.tiles[(m, n)]

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return self.width * self.height

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        x = random.random() * self.width
        y = random.random() * self.height
        return Position(x, y)


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """

    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the
        specified room. The robot initially has a random direction and a random
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot
                  in a single time-step
        """
        self.room = room
        self.speed = speed
        self.capacity = capacity
        self.position = room.get_random_position()
        self.direction = random.randint(0, BIG_THETA)

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position (if the new position is invalid,
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead*
    chooses a new direction randomly.
    """

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position (if the new position is invalid,
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity.
        """
        # Calculates the new position
        new_pos = self.position.get_new_position(self.direction, self.speed)
        # Checks if the position is valid
        if self.room.is_position_in_room(new_pos):
            self.set_robot_position(new_pos)
            m, n = math.floor(new_pos.get_x()), math.floor(new_pos.get_y())
            # If it is valid and the room is not cleaned
            if not self.room.is_tile_cleaned(m, n):
                self.room.clean_tile_at_position(new_pos, self.capacity)
        # If the position is not valid it will change the robot direction randomly
        else:
            self.set_robot_direction(random.randint(0, BIG_THETA))


# Uncomment this line to see your implementation of StandardRobot in action!
# test_robot_movement(StandardRobot, RectangularRoom)


# === Problem 3
class RobotWithACat(Robot):
    """
    A RobotWithACat is a robot with a cat mounted on it. A RobotWithACat will
    not clean the tile it moves to and pick a new, random direction for itself
    with probability p rather than simply cleaning the tile it moves to.
    """
    p = 0.1337
    def __init__(self, room, speed, capacity):
        Robot.__init__(self, room, speed, capacity)
        self.set_cat_probability(self.p)

    @staticmethod
    def set_cat_probability(prob):
        """
        Sets the probability of the cat messing with the controls equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        RobotWithACat.p = prob


    def gets_cat_interference(self):
        """
        Answers the question: Does the cat mess with this RobotWithACat's controls
        at this timestep?
        The cat messes with the RobotWithACat's controls with probability p.

        returns: True if the cat messes with RobotWithACat's controls, False otherwise.
        """
        return random.random() < RobotWithACat.p

    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the cat messes with the controls. If the robot does get cat
        interference, do not clean the current tile and change its direction randomly.

        If the cat does not mess with the controls, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        # Checks if cat is messing with the robot
        if self.gets_cat_interference():
            self.set_robot_direction(random.randint(0,BIG_THETA))
        # If it's not messing it will do the same as the standard robot
        else:
            # Calculates the new position
            new_pos = self.position.get_new_position(self.direction, self.speed)
            # Checks if the position is valid
            if self.room.is_position_in_room(new_pos):
                self.set_robot_position(new_pos)
                m, n = math.floor(new_pos.get_x()), math.floor(new_pos.get_y())
                # If it is valid and the room is not cleaned
                if not self.room.is_tile_cleaned(m, n):
                    self.room.clean_tile_at_position(new_pos, self.capacity)
            # If the position is not valid it will change the robot direction randomly
            else:
                self.set_robot_direction(random.randint(0, BIG_THETA))


#test_robot_movement(RobotWithACat, RectangularRoom)

# === Problem 4
class SuperRobot(Robot):
    """
    A SuperRobot is a robot that moves extra fast and cleans two tiles in one timestep.

    It moves in its current direction, cleans the tile it lands on, and continues
    moving in that direction and cleans the second tile it lands on, all in one unit of time.

    If the SuperRobot hits a wall when it attempts to move in its current direction,
    it may dirty the current tile by one unit because it moves very fast and can knock dust off of the wall.

    There are three possible cases:

    1. The robot tries to move. If it would hit the wall on the first move, it
    does not move. Instead, it turns to face a random direction and stops for this timestep.

    2. If it can move, it moves and cleans the tile it moves to. Then, it tries to move a second time.

        a. If it hits the wall with probability p it dirties the tile its on and turns to a random direction
           Then it stops.

        b. If it does not hit the wall, it moves and cleans the tile it moves to.

    """
    p = 0.15
    def __init__(self, room, speed, capacity):
        Robot.__init__(self, room, speed, capacity)
        self.set_dirty_probability(self.p)

    @staticmethod
    def set_dirty_probability(prob):
        """
        Sets the probability of getting the tile dirty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        SuperRobot.p = prob

    def dirties_tile(self):
        """
        Answers the question: Does this SuperRobot dirty the tile if it hits the wall at full speed?
        A SuperRobot dirties a tile with probability p.

        returns: True if the SuperRobot dirties the tile, False otherwise.
        """
        return random.random() < SuperRobot.p

    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot is going to hit a wall when it tries moving to the second tile.
        If it is, clean the tile adjacent to the wall and then dirty it by 1 unit with probability p,
        and rotate to a random direction.

        If the robot is not going to run into a wall when going to the second tile, the robot should
        behave like StandardRobot, but move two tiles at a time (checking if it can move to both new
        positions and move there if it can, or pick a new direction and stay stationary if it is adjacent
        to a wall)
        """
        # Gets the new position
        new_pos = self.position.get_new_position(self.direction, self.speed)
        # If the new position is in room it will move and clean it
        if self.room.is_position_in_room(new_pos):
            self.set_robot_position(new_pos)
            m, n = math.floor(new_pos.get_x()), math.floor(new_pos.get_y())
            # If it is valid and the room is not cleaned
            if not self.room.is_tile_cleaned(m, n):
                self.room.clean_tile_at_position(new_pos, self.capacity)
            # Gets the new new postion
            new_new_pos = self.position.get_new_position(self.direction, self.speed)
            m, n = math.floor(new_new_pos.get_x()), math.floor(new_new_pos.get_y())
            # If it is in the room it will clean it
            if self.room.is_position_in_room(new_new_pos):
                self.set_robot_position(new_new_pos)
                # If it is valid and the room is not cleaned
                if not self.room.is_tile_cleaned(m, n):
                    self.room.clean_tile_at_position(new_new_pos, self.capacity)
            # If it's not in the room it will make it dirty with probability p
            else:
                if self.dirties_tile():
                    self.room.clean_tile_at_position(new_pos, -1)
                # Then it will rotate
                self.set_robot_direction(random.randint(0, BIG_THETA))
        # Rotate
        else:
            self.set_robot_direction(random.randint(0,BIG_THETA))


# test_robot_movement(SuperRobot, RectangularRoom)
# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                   robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room. For example,
    if we want to test the amount of time it takes to clean 75% of the room, min_coverage
    would be 0.75.

    The simulation is run with num_robots robots of type robot_type, each
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RobotWithACat)
    """
    delay = .05
    sum_time_steps = 0
    # Run the simulation num_trials times
    for i in range(num_trials):
        # anim = ps3_visualize.RobotVisualization(num_robots, width, height, delay)
        # Creates a room
        room = RectangularRoom(width, height, dirt_amount)
        robots = []
        # Creates a list of robots
        for robot_num in range(num_robots):
            robots.append(robot_type(room, speed, capacity))
        num_tiles = room.get_num_tiles()
        step = 0
        # Clean the room until the room is cleaned with the amount of mean coverage
        while room.get_num_cleaned_tiles()/num_tiles < min_coverage:
            # print('coverage : ', room.get_num_cleaned_tiles()/num_tiles)
            step += 1
            for robot in robots:
                robot.update_position_and_clean()
            # anim.update(room, robots)
        sum_time_steps += step
        # anim.done()
    # Calculates the mean_step
    mean_step = sum_time_steps/num_trials
    return mean_step




# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the three robot types compare when cleaning 80%
#       of a 20x20 room?
#   Super robot is faster than the other and catrobot is slower but cat and standard converge to the same number of
#   steps as number of robots increase. and Super robot converges to the less number of time steps than the other two.
#
#
# 2) How does the performance of the three robot types compare when two of each
#       robot cleans 80% of rooms with dimensions
#       10x30, 20x15, 25x12, and 50x6?
#   The number of time steps for standard robot and SuperRobot stays roughly the same for different dimensions of the
#   room but the CatRobot is not quite consistent in the number of steps. Also, the number of steps required for Super
#   is almost half of the StandardRobot and CatRobot takes the longest to clean.
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the three robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, RobotWithACat))
        times3.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, SuperRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RobotWithACat', 'SuperRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [10, 20, 25, 50]:
        height = int(300 / width)
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, RobotWithACat))
        times3.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, SuperRobot))
    pylab.plot(aspect_ratios, times1, 'o-')
    pylab.plot(aspect_ratios, times2, 'o-')
    pylab.plot(aspect_ratios, times3, 'o-')
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RobotWithACat', 'SuperRobot'), fancybox=True, framealpha=0.5)
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
