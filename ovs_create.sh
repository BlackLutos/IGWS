#!/bin/bash
ovs-vsctl add-br ovs-br0
ovs-vsctl add-br ovs-br1
ovs-vsctl set-controller ovs-br0 tcp:127.0.0.1:6633
ovs-vsctl set-controller ovs-br1 tcp:127.0.0.1:6633
ip link add ovs-br0-eth1 type veth peer name ovs-br1-eth1
ovs-vsctl add-port ovs-br0 ovs-br0-eth1
ovs-vsctl add-port ovs-br1 ovs-br1-eth1
ifconfig ovs-br0-eth1 up
ifconfig ovs-br1-eth1 up
# ovs-vsctl set bridge ovs-br0 protocol=OpenFlow13
# ovs-vsctl -- set bridge ovs-br0 fail-mode=standalone
# ovs-vsctl -- set bridge ovs-br0 fail-mode=secure
ovs-vsctl show
# --protocols=Openflow13
exec bash
