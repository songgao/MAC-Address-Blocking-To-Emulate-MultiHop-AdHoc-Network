#!/usr/bin/python2.7

import sys
import os
import time
import pickle
import commands
import memcache

sys.path.append('../include')
from configurations import *
from get_nodes import get_nodes
from MNode import MNode
from set_pairs import set_pairs_by_nodes_and_pairs_filename

def __continue(mc):
    # decide whether the program should continue running
    return True
    # return mc.get('sheldon_exit') in (None, 0)

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
    # print "Setting up nodes' pairs"
    # set_pairs_by_nodes_and_pairs_filename(nodes, sys.argv[2]);
    for node_key in nodes:
        m_nodes[node_key] = MNode()
    print "All set up. Setting locations."
    flag = True
    for key, m_node in m_nodes.items():
        if flag:
            m_node.x = 360
            m_node.y = 360
            flag = False
        else:
            m_node.x = 120
            m_node.y = 120
        mc.set(key, m_node.to_memcached_str())


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage:", sys.argv[0], "[nodes config file]"
    else:
        main()
