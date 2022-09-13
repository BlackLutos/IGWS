#!/bin/bash
ovs-vsctl del-br ovs-br0
ovs-vsctl del-controller ovs-br0
exec bash