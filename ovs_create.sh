#!/bin/bash
ovs-vsctl add-br ovs-br0
ovs-vsctl set-controller ovs-br0 tcp:127.0.0.1:6633
# ovs-vsctl set bridge ovs-br0 protocol=OpenFlow13
# ovs-vsctl -- set bridge ovs-br0 fail-mode=standalone
# ovs-vsctl -- set bridge ovs-br0 fail-mode=secure
ovs-vsctl show
# --protocols=Openflow13
exec bash
