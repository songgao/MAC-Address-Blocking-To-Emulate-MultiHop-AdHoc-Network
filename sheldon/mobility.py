import random
import math

from configurations import *
from MNode import MNode

def __find_grid_points(grid_points, start, end):
    # to find the first point in grid_points that lies between start & end. returns None if not found
    min_p, max_p = min(start, end), max(start, end)
    r = None
    for point in grid_points:
        if point != start and min_p <= point and point <= max_p:
            if r == None:
                r = point
            else:
                if math.fabs(r - start) > math.fabs(point - start):
                    r = point
    return r

def move_m_node(m_node):
    if m_node.direction == MNode.EAST:
        new_x = m_node.x + m_node.speed * UPDATE_INTERVAL
        grid_point = __find_grid_points(GRID_POINTS_X, m_node.x, new_x)
        if grid_point != None:
            rand = random.uniform(0,1)
            if rand < PROB_TURN or (new_x >= max(GRID_POINTS_X)):
                if m_node.y == min(GRID_POINTS_Y):
                    m_node.direction = MNode.NORTH
                elif m_node.y == max(GRID_POINTS_Y):
                    m_node.direction = MNode.SOUTH
                elif rand < PROB_TURN / 2:
                    m_node.direction = MNode.NORTH
                else:
                    m_node.direction = MNode.SOUTH
            new_x = grid_point
        m_node.x = new_x
        
    elif m_node.direction == MNode.SOUTH:
        new_y = m_node.y - m_node.speed * UPDATE_INTERVAL
        grid_point = __find_grid_points(GRID_POINTS_Y, m_node.y, new_y)
        if grid_point != None:
            rand = random.uniform(0,1)
            if rand < PROB_TURN or (new_y <= min(GRID_POINTS_Y)):
                if m_node.x == min(GRID_POINTS_X):
                    m_node.direction = MNode.EAST
                elif m_node.x == max(GRID_POINTS_X):
                    m_node.direction = MNode.WEST
                elif rand < PROB_TURN / 2:
                    m_node.direction = MNode.EAST
                else:
                    m_node.direction = MNode.WEST
            new_y = grid_point
        m_node.y = new_y
 
    elif m_node.direction == MNode.WEST:
        new_x = m_node.x - m_node.speed * UPDATE_INTERVAL
        grid_point = __find_grid_points(GRID_POINTS_X, m_node.x, new_x)
        if grid_point != None:
            rand = random.uniform(0,1)
            if rand < PROB_TURN or (new_x <= min(GRID_POINTS_X)):
                if m_node.y == min(GRID_POINTS_Y):
                    m_node.direction = MNode.NORTH
                elif m_node.y == max(GRID_POINTS_Y):
                    m_node.direction = MNode.SOUTH
                elif rand < PROB_TURN / 2:
                    m_node.direction = MNode.SOUTH
                else:
                    m_node.direction = MNode.NORTH
            new_x = grid_point
        m_node.x = new_x
 
    elif m_node.direction == MNode.NORTH:
        new_y = m_node.y + m_node.speed * UPDATE_INTERVAL
        grid_point = __find_grid_points(GRID_POINTS_Y, m_node.y, new_y)
        if grid_point != None:
            rand = random.uniform(0,1)
            if rand < PROB_TURN or (new_y >= max(GRID_POINTS_Y)):
                if m_node.x == min(GRID_POINTS_X):
                    m_node.direction = MNode.EAST
                elif m_node.x == max(GRID_POINTS_X):
                    m_node.direction = MNode.WEST
                elif rand < PROB_TURN / 2:
                    m_node.direction = MNode.WEST
                else:
                    m_node.direction = MNode.EAST
            new_y = grid_point
        m_node.y = new_y
