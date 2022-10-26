import json
import os
import sh
import requests

def get_if_port(if_name):
    if_port = os.popen('sudo ovs-vsctl list interface | grep ' + if_name + ' -A 1 | tail -n 1 | awk \'{print $(NF)}\'').read()
    if_port = if_port.split('\n')[0]
    return int(if_port)

def add_flow():
    with open('wan_detect/link_info.json') as f:
        link_info = json.load(f)
    with open('flow1.json') as f:
        flow1 = json.load(f)
    with open('flow2.json') as f:
        flow2 = json.load(f)
    with open('flow3.json') as f:
        flow3 = json.load(f)
    with open('flow4.json') as f:
        flow4 = json.load(f)

    flow1_dpid = flow1['dpid']
    flow1_out_port = flow1['actions'][0]['port']
    flow1_in_port = flow1['match']['in_port']

    eth_port = 'br-eth3'

    ovs_dpid = [i for i in link_info.keys()]
    flow1['dpid'] = ovs_dpid[1]
    flow2['dpid'] = ovs_dpid[1]
    flow3['dpid'] = ovs_dpid[0]
    flow4['dpid'] = ovs_dpid[0]

    flow1['match']['in_port'] = get_if_port(eth_port)
    flow2['match']['in_port'] = get_if_port('ovs-br0-eth1')
    flow3['match']['in_port'] = get_if_port('ovs-br1-eth1')
    flow4['match']['in_port'] = 'LOCAl'

    flow1['actions'][0]['port'] = get_if_port('ovs-br0-eth1')
    flow2['actions'][0]['port'] = get_if_port('br-eth3')
    flow3['actions'][0]['port'] = 'NORMAL'
    flow4['actions'][0]['port'] = get_if_port('ovs-br1-eth1')

    with open('flow1.json','w') as f:
        f.write(json.dumps(flow1))
    with open('flow2.json','w') as f:
        f.write(json.dumps(flow2))
    with open('flow3.json','w') as f:
        f.write(json.dumps(flow3))
    with open('flow4.json','w') as f:
        f.write(json.dumps(flow4))

# if __name__=='__main__':
#     add_flow()
#     sh.bash('add_flow.sh')

# sh.curl('-X POST -H 'Content-Type: application/json' -d @flow1.json http://127.0.0.1:8080/stats/flowentry/add')
# sh.curl(' -X POST -H \'Content-Type: application/json\' -d @flow2.json http://127.0.0.1:8080/stats/flowentry/add')
# sh.curl(' -X POST -H \'Content-Type: application/json\' -d @flow3.json http://127.0.0.1:8080/stats/flowentry/add')
# sh.curl(' -X POST -H \'Content-Type: application/json\' -d @flow4.json http://127.0.0.1:8080/stats/flowentry/add')