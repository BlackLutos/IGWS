#!/bin/bash
sudo nmcli connection delete br0
sudo nmcli connection delete bridge-slave-eth0
ovs-vsctl del-br ovs-br0
ovs-vsctl del-controller ovs-br0
ovs-vsctl show