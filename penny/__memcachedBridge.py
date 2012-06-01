import sys
import pickle
import memcache

sys.path.append('../include')
from configurations import *
from MNode import MNode

def getInfo():
    r = {}
    mc = memcache.Client([MEMCACHED_ADDR + ':' + MEMCACHED_PORT], debug = 0)
    nodes = pickle.loads(mc.get('nodes'))
    r['nodes'] = nodes
    r['grid_points_x'] = GRID_POINTS_X
    r['grid_points_y'] = GRID_POINTS_Y
    return r

def getGeoAndTopo():
    mc = memcache.Client([MEMCACHED_ADDR + ':' + MEMCACHED_PORT], debug = 0)
    nodes = pickle.loads(mc.get('nodes'))
    r = {}
    for node_key in nodes:
        n = {}
        m_node = MNode(mc.get(node_key))
        n['speed'] = m_node.speed
        n['x'] = m_node.x
        n['y'] = m_node.y
        n['direction'] = m_node.get_direction_in_str();
        n['neighbors'] = pickle.loads(mc.get('neighbors_' + node_key))
        r[node_key] = n
    return r
