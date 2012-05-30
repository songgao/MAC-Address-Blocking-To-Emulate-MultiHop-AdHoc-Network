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
from mobility import move_m_node

def __continue(mc):
    # decide whether the program should continue running
    return mc.get('sheldon_exit') in (None, 0)

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
    while __continue(mc):
        for key, m_node in m_nodes.items():
            move_m_node(m_node)
            mc.set(key, m_node.to_memcached_str())
        time.sleep(UPDATE_INTERVAL)
    mc.set('sheldon_exit', 0)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage:", sys.argv[0], "[nodes config file] [pairs config file]"
    else:
        main()
