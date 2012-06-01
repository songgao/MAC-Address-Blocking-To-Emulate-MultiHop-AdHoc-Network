import random

from configurations import *

class MNode:

    # directions
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def __init__(self, memcached_str = None):
        if(memcached_str == None):
            if random.uniform(0,1) < 0.5:
                # on grid rows
                self.y = random.choice(GRID_POINTS_Y)
                self.x = random.uniform(min(GRID_POINTS_X), max(GRID_POINTS_X))
            else:
                # on grid columns
                self.x = random.choice(GRID_POINTS_X)
                self.y = random.uniform(min(GRID_POINTS_Y), max(GRID_POINTS_Y))
            self.speed = random.uniform(MIN_SPEED, MAX_SPEED)
            self.direction = random.randint(0, 3)
        else:
            values = memcached_str.split()
            self.x = float(values[0])
            self.y = float(values[1])
            self.speed = float(values[2])
            self.direction = float(values[3])

    def to_memcached_str(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.speed) + " " + str(self.direction)

    def update_from_memcached_str(self, memcached_str):
        values = memcached_str.split()
        self.x = float(values[0])
        self.y = float(values[1])
        self.speed = float(values[2])
        self.direction = float(values[3])

    def get_direction_in_str(self):
        if self.direction == MNode.EAST:
            return 'E'
        elif self.direction == MNode.WEST:
            return 'W'
        elif self.direction == MNode.NORTH:
            return 'N'
        elif self.direction == MNode.SOUTH:
            return 'S'
        else:
            return None
