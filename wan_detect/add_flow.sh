#!/bin/bash
curl -X POST -H 'Content-Type: application/json' -d @flow1.json http://127.0.0.1:8080/stats/flowentry/add
curl -X POST -H 'Content-Type: application/json' -d @flow2.json http://127.0.0.1:8080/stats/flowentry/add
curl -X POST -H 'Content-Type: application/json' -d @flow3.json http://127.0.0.1:8080/stats/flowentry/add
curl -X POST -H 'Content-Type: application/json' -d @flow4.json http://127.0.0.1:8080/stats/flowentry/add