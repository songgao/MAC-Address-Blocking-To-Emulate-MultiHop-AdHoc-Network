import commands
from configurations import *

def get_mac(hostname):
    return commands.getstatusoutput('ssh ' + NODES_USERNAME + '@' + hostname + " ip addr show dev " + NODES_IF_OLSR + " | grep link/ether | awk '{print $2}'")[1]

def get_nodes(nodes_file):
    f = open(nodes_file, 'r')
    nodes = {}
    for l in f:
        if not l or l.isspace() or len(l.strip()) == 0 or l.strip().startswith('#'):
            continue;
        values = l.strip().split()
        node_inf= {}
        node_inf['eth0'] = values[1]
        node_inf['eth1'] = values[2]
        node_inf['eth2'] = values[3]
        print 'Getting OLSR mac address for node', values[0]
        node_inf['olsr_mac'] = get_mac(values[1])
        nodes[values[0]] = node_inf
    return nodes
