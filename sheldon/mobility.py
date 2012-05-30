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
            new_x = grid_point
            rand = random.uniform(0,1)
            if rand < PROB_TURN:
                if rand < PROB_TURN / 2:
                    m_node.direction = MNode.NORTH
                else:
                    m_node.direction = MNode.SOUTH
        m_node.x = new_x
        while m_node.x > max(GRID_POINTS_X):
            m_node.x = m_node.x - (max(GRID_POINTS_X) - min(GRID_POINTS_X))
        while m_node.x < min(GRID_POINTS_X):
            m_node.x = m_node.x + (max(GRID_POINTS_X) - min(GRID_POINTS_X))
        
    elif m_node.direction == MNode.SOUTH:
        new_y = m_node.y - m_node.speed * UPDATE_INTERVAL
        grid_point = __find_grid_points(GRID_POINTS_Y, m_node.y, new_y)
        if grid_point != None:
            new_y = grid_point
            rand = random.uniform(0,1)
            if rand < PROB_TURN:
                if rand < PROB_TURN / 2:
                    m_node.direction = MNode.EAST
                else:
                    m_node.direction = MNode.WEST
        m_node.y = new_y
        while m_node.y > max(GRID_POINTS_Y):
            m_node.y = m_node.y - (max(GRID_POINTS_Y) - min(GRID_POINTS_Y))
        while m_node.y < min(GRID_POINTS_X):
            m_node.y = m_node.y + (max(GRID_POINTS_Y) - min(GRID_POINTS_Y))
 
    elif m_node.direction == MNode.WEST:
        new_x = m_node.x - m_node.speed * UPDATE_INTERVAL
        grid_point = __find_grid_points(GRID_POINTS_X, m_node.x, new_x)
        if grid_point != None:
            new_x = grid_point
            rand = random.uniform(0,1)
            if rand < PROB_TURN:
                if rand < PROB_TURN / 2:
                    m_node.direction = MNode.SOUTH
                else:
                    m_node.direction = MNode.NORTH
        m_node.x = new_x
        while m_node.x > max(GRID_POINTS_X):
            m_node.x = m_node.x - (max(GRID_POINTS_X) - min(GRID_POINTS_X))
        while m_node.x < min(GRID_POINTS_X):
            m_node.x = m_node.x + (max(GRID_POINTS_X) - min(GRID_POINTS_X))
 
    elif m_node.direction == MNode.NORTH:
        new_y = m_node.y + m_node.speed * UPDATE_INTERVAL
        grid_point = __find_grid_points(GRID_POINTS_Y, m_node.y, new_y)
        if grid_point != None:
            new_y = grid_point
            rand = random.uniform(0,1)
            if rand < PROB_TURN:
                if rand < PROB_TURN / 2:
                    m_node.direction = MNode.WEST
                else:
                    m_node.direction = MNode.EAST
        m_node.y = new_y
        while m_node.y > max(GRID_POINTS_Y):
            m_node.y = m_node.y - (max(GRID_POINTS_Y) - min(GRID_POINTS_Y))
        while m_node.y < min(GRID_POINTS_Y):
            m_node.y = m_node.y + (max(GRID_POINTS_Y) - min(GRID_POINTS_Y))


