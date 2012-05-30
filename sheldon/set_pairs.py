#!/usr/bin/python2.7

import commands
import sys

from get_nodes import get_nodes
from configurations import *

def set_pairs(nodes, pairs):
    for pair in pairs:
        ports = ['9146', '9147', '9148', '9149']
        cmd0 = "echo 'Setting up pair forwarding.'"
        cmd1 = "echo 'Setting up pair forwarding.'"
        for port in ports:
            cmd0 = cmd0 + " && iptables -t nat --flush && iptables -t nat -A PREROUTING -p tcp --dport " + port + " -d " + nodes[pair[0]][NODES_IF_OLSR] + " -j DNAT --to " + nodes[pair[1]][NODES_IF_FORWARD] + ":" + port + " && iptables -t nat -A POSTROUTING -p tcp --dport " + port + " -d " + nodes[pair[1]][NODES_IF_FORWARD] + " -j SNAT --to " + nodes[pair[0]][NODES_IF_OLSR]
            cmd1 = cmd1 + " && iptables -t nat --flush && iptables -t nat -A PREROUTING -p tcp --dport " + port + " -d " + nodes[pair[1]][NODES_IF_OLSR] + " -j DNAT --to " + nodes[pair[0]][NODES_IF_FORWARD] + ":" + port + " && iptables -t nat -A POSTROUTING -p tcp --dport " + port + " -d " + nodes[pair[0]][NODES_IF_FORWARD] + " -j SNAT --to " + nodes[pair[1]][NODES_IF_OLSR]
        s0 = commands.getstatusoutput('ssh ' + NODES_USERNAME + '@' + nodes[pair[0]][NODES_IF_CONTROL] + " '" + cmd0 + "'")[0]
        s1 = commands.getstatusoutput('ssh ' + NODES_USERNAME + '@' + nodes[pair[1]][NODES_IF_CONTROL] + " '" + cmd1 + "'")[0]
        if s0 == 0 and s1 == 0:
            print pair, ' SUCCESS'
        else:
            print pair, ' FAILED'

def set_pairs_by_nodes_and_pairs_filename(nodes, pairs_file):
    f = open(pairs_file, 'r')
    pairs=[]
    for l in f:
        if not l or l.isspace() or len(l.strip()) == 0 or l.strip().startswith('#'):
            continue;
        line = l.strip()
        pairs.append( (line.split()[0], line.split()[1]) )
    set_pairs(nodes, pairs)

def set_pairs_by_filenames(nodes_file, pairs_file):
    set_pairs_by_nodes_and_pair_filename(get_nodes(nodes_file), pairs_file)

if __name__ == '__main__':
    set_pairs_by_filenames(sys.argv[1], sys.argv[2])
