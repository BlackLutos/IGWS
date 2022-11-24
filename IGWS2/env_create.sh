#!/bin/bash
ovs-vsctl add-br ovs-br1
ovs-vsctl set-controller ovs-br1 tcp:172.30.1.32:6653
ovs-vsctl add-port ovs-br1 eth1
ovs-vsctl show