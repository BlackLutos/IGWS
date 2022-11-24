#!/bin/bash
sshpass -p "raspberry" ssh pi@172.30.1.171 'sudo ifconfig ovs-br1 192.168.0.1/24 up'