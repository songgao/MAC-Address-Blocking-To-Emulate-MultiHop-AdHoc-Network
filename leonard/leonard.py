#!/usr/bin/python2.7

import sys
import os
import time
import pickle
import commands
import memcache

sys.path.append('../include')
from configurations import *
from MNode import MNode

def __distance_squared(x0, y0, x1, y1):
    return (y1 - y0) * (y1 - y0) + (x1 - x0) * (x1 - x0)

def __set_mac_filtering(my_key, nodes, m_nodes):
    blocked_mac = []
    me = nodes[my_key]
    m_me = m_nodes[my_key]
    for key, m_node in m_nodes.items():
        if key != my_key:
            if __distance_squared(float(m_node.x), float(m_node.y), float(m_me.x), float(m_me.y)) > COMMUNICATION_RANGE * COMMUNICATION_RANGE:
                blocked_mac.append(nodes[key]['olsr_mac'].lower())
    current_iptables_listing = commands.getstatusoutput('iptables -L')[1].splitlines();
    current_blocked_mac = []
    for line in current_iptables_listing:
        if len(line.split()) >= 6 and line.split()[5] == 'MAC':
            current_blocked_mac.append(line.split()[6].lower())
    for mac in blocked_mac:
        if mac not in current_blocked_mac:
            commands.getstatusoutput("iptables -A INPUT -m mac --mac-source " + mac + " -j DROP")
    for mac in current_blocked_mac:
        if mac not in blocked_mac:
            commands.getstatusoutput("iptables -D INPUT -m mac --mac-source " + mac + " -j DROP")

def __inform_memcached_about_neighbor_links(my_key, mc, nodes):
    neighbors = []
    neighbors_str = commands.getstatusoutput('ip route show dev ' + NODES_IF_OLSR + ' | grep link')[1]
    for neighbor_str in neighbors_str.splitlines():
        if not neighbor_str or neighbor_str.isspace() or len(neighbor_str.strip()) == 0 or ('/' in neighbor_str):
            continue
        addr = neighbor_str.split()[0]
        for key, node in nodes.items():
            if addr == node[NODES_IF_OLSR]:
                neighbors.append(key)
                break
    mc.set('neighbors_' + my_key, pickle.dumps(neighbors))

def __find_myself(nodes):
    eth0_addr = commands.getstatusoutput("ip addr show dev eth0 | grep 'inet ' | awk '{print $2}'")[1].split('/')[0]
    for key, node in nodes.items():
        if node['eth0'] == eth0_addr:
            return key
    return None

def main():
    commands.getstatusoutput('iptables --flush')
    if commands.getstatusoutput("iptables -L")[0] != 0:
        print 'iptables command test failed. Are you sure I am running with root permission?'
        exit(1)
    mc = memcache.Client([MEMCACHED_ADDR + ':' + MEMCACHED_PORT], debug = 0)
    nodes = pickle.loads(mc.get('nodes'))
    my_key = __find_myself(nodes)
    if my_key == None:
        print "I don't have an identity.. T.T"
        exit(1)
    m_nodes = {}
    for node_key in nodes:
        m_nodes[node_key] = MNode(mc.get(node_key))
    print 'Forking into background.'
    if os.fork() !=0:
        exit(0)
    while True:
        leonard_exit = mc.get('leonard_exit')
        if leonard_exit in (None, 0):
            mc.set('leonard_exit', leonard_exit - 1)
            break;
        for key, m_node in m_nodes.items():
            m_node.update_from_memcached_str(mc.get(key))
        __set_mac_filtering(my_key, nodes, m_nodes)
        __inform_memcached_about_neighbor_links(my_key, mc, nodes)
        time.sleep(UPDATE_INTERVAL)

if __name__ == '__main__':
    main()
