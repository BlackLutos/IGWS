#!/bin/bash
sudo nmcli con add ifname br0 type bridge con-name br0
nmcli con add type bridge-slave ifname eth0 master br0
sudo nmcli con modify br0 bridge.stp no
sudo nmcli con modify br0 ipv4.addresses '192.168.0.1/24'
sudo nmcli con modify br0 ipv4.method manual
sudo nmcli con up br0
sudo nmcli con up bridge-slave-eth0
ifconfig eth0 up
sysctl -w net.ipv4.ip_forward=1
sysctl -p
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o wlan0 -j MASQUERADE
ovs-vsctl add-br ovs-br0
ovs-vsctl set-controller ovs-br0 tcp:172.30.1.32:6653
ovs-vsctl add-port ovs-br0 eth1
ovs-vsctl show