#!/usr/bin/python2.7

import commands
import sys

from get_nodes import get_nodes
from configurations import *

def set_pairs(nodes, pairs):
    for pair in pairs:
        ports = ['9146', '9147', '9148', '9149']
        cmd0 = "iptables -t nat --flush"
        cmd1 = "iptables -t nat --flush"
        for port in ports:
            # tcp forwarding on pair[0]
            cmd0 = cmd0 + " && iptables -t nat -A PREROUTING -i " + NODES_IF_OLSR + " -p tcp --dport " + port + " -j DNAT --to " + nodes[pair[1]][NODES_IF_FORWARD] + ":" + port
            # udp forwarding on pair[0]
            cmd0 = cmd0 + " && iptables -t nat -A PREROUTING -i " + NODES_IF_OLSR + " -p udp --dport " + port + " -j DNAT --to " + nodes[pair[1]][NODES_IF_FORWARD] + ":" + port
            # tcp forwarding on pair[1]
            cmd1 = cmd1 + " && iptables -t nat -A PREROUTING -i " + NODES_IF_OLSR + " -p tcp --dport " + port + " -j DNAT --to " + nodes[pair[0]][NODES_IF_FORWARD] + ":" + port
            # udp forwarding on pair[1]
            cmd1 = cmd1 + " && iptables -t nat -A PREROUTING -i " + NODES_IF_OLSR + " -p udp --dport " + port + " -j DNAT --to " + nodes[pair[0]][NODES_IF_FORWARD] + ":" + port
        # MASQUERADE on pair[0]
        cmd0 = cmd0 + " && iptables -t nat -A POSTROUTING -o " + NODES_IF_FORWARD + " -j MASQUERADE"
        # MASQUERADE on pair[1]
        cmd1 = cmd1 + " && iptables -t nat -A POSTROUTING -o " + NODES_IF_FORWARD + " -j MASQUERADE"
        s0 = commands.getstatusoutput('ssh ' + NODES_USERNAME + '@' + nodes[pair[0]][NODES_IF_CONTROL] + " '" + cmd0 + "'")[0]
        s1 = commands.getstatusoutput('ssh ' + NODES_USERNAME + '@' + nodes[pair[1]][NODES_IF_CONTROL] + " '" + cmd1 + "'")[0]
        if s0 == 0 and s1 == 0:
            print pair, ' SUCCESS'
        else:
            print pair, ' FAILED', s0, s1

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
