#!/usr/bin/python2.7

import sys
import os
import random
import time
import math
import pickle
import commands
import memcache

from configurations import *
from get_nodes import get_nodes
from MNode import MNode
from set_pairs import set_pairs_by_nodes_and_pairs_filename

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

def __move_m_node(m_node):
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

def __continue():
    # decide whether the program should continue running
    return True;

def __ensure_memcached_is_running():
    if commands.getstatusoutput('netstat -l|grep ' + MEMCACHED_PORT)[1] == '':
        r = commands.getstatusoutput('memcached -d -l ' + MEMCACHED_ADDR + ' -p ' + MEMCACHED_PORT + ' -u ' + MEMCACHED_USERNAME)

def main():
    __ensure_memcached_is_running()
    mc = memcache.Client([MEMCACHED_ADDR + ':' + MEMCACHED_PORT], debug = 0)
    m_nodes = {}
    print "Gathering nodes' information"
    nodes = get_nodes(sys.argv[1])
    mc.set('nodes', pickle.dumps(nodes))
    print "Setting up nodes' pairs"
    set_pairs_by_nodes_and_pairs_filename(nodes, sys.argv[2]);
    for node_key in nodes:
        m_nodes[node_key] = MNode()
    print "All set up. Forking to background."
    if os.fork() != 0:
        exit(0)
    print "Entering mobility loop."
    while __continue():
        for key, m_node in m_nodes.items():
            __move_m_node(m_node)
            mc.set(key, m_node.to_memcached_str())
        time.sleep(UPDATE_INTERVAL)

if __name__ == '__main__':
    main()
