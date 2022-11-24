#!/bin/bash
sshpass -p "raspberry" ssh pi@172.30.1.171 'sudo ifconfig ovs-br1 192.168.0.1/24 up'
curl -X POST -H 'Content-Type: application/json' -d @flow1.json http://127.0.0.1:8080/stats/flowentry/add
curl -X POST -H 'Content-Type: application/json' -d @flow2.json http://127.0.0.1:8080/stats/flowentry/add
curl -X POST -H 'Content-Type: application/json' -d @flow3.json http://127.0.0.1:8080/stats/flowentry/add
curl -X POST -H 'Content-Type: application/json' -d @flow4.json http://127.0.0.1:8080/stats/flowentry/add