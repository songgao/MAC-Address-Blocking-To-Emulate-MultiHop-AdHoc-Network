# MAC-Address-Blocking-To-Emulate-MultiHop-AdHoc-Network

This repository consists of some python scripts that help emulate multi-hop AdHoc networks on ethernet.

It operates on each node and uses iptables MAC address blocking to form a multi-hop topology based on each node's virtual position. It's useful to perceive how a routing daemon (e.g. olsrd) react to topology change, and measure how much bandwidth it's gonna use for different parameter set.

`sheldon` contains a simple mobility simulator that assigns and maintains positions of nodes on a grid map;

`leonard` operates on each node. It reads position data that `sheldon` maintains and based on it set up MAC address blocking regarding to every other node.

`penny` is a simple web GUI that visualize the grid map and every nodes on it. It also shows topology between nodes by looking up IP routing table on each node.


**This project only does blocking, but does not consider channel congestion or interference in wireless networks. For emulation more close to realistic, including channel congestion, hidden station, etc., take a look at [squirrel](http://songgao.github.com/squirrel/).**

This was built in Spring 2012, and is not being maintained any more. Use it however you want, but share-alike if possible.
