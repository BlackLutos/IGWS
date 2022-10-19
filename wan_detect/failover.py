import os
import sh
import glob
import json

def get_br_port():
    # port = 'bridge-slave-br-' + input_port
    data = glob.glob(r"/etc/NetworkManager/system-connections/*")
    br_port = []
    for i in data:
        br_port.append(i.split('/etc/NetworkManager/system-connections/')[1])
    br_port.remove('br0')
    return br_port
    
def ovs_port_select():
    # port = input("Please input port number (like ex. eth3): ")
    with open('config.json','r') as f:
        config = json.load(f)
    port = config['ovs_port_select'] 
    #judge if exist 
    return str(port)
    #list of interface 
    #/etc/NetworkManager/system-connections

# if __name__=='__main__':
def failover():
    # os.system('brctl show') 
    # os.system('nmcli connection show')
    #network manager
    # os.system('ovs-vsctl show')
    print('-------------------------------------------------------------------')

    exist_port_list = get_br_port()
    print('Exist Bridge Port List\n')
    print('S/N' + '     ' + 'Bridge Name')
    port_num = 1
    for i in exist_port_list:
        str_port_num = str(port_num)
        print(str_port_num + '.      ' + i)
        port_num += 1
    print('\n')

    port_is_exist = True
    while(port_is_exist):
        port = ovs_port_select()
        br_port = 'bridge-slave-br-' + port
        br_port_list = get_br_port()
        if br_port not in br_port_list:
            print('Error! Port: ' + port + ' is not exist, ' + 'please input the correct eth-port number again.')
        else:
            port_is_exist = False
            break

    eth_port = 'br-' + port
    h_eth_port = 'h-' + port
    # sudo nmcli con up bridge-slave-br-eth3
    diable_eth_port = 'nmcli con down ' + 'bridge-slave-' + eth_port
    del_eth_port = 'sudo nmcli connection delete ' + br_port
    ovs_add_port = 'ovs-vsctl add-port ovs-br0 ' + eth_port

    os.system(diable_eth_port)
    os.system(del_eth_port)
    os.system(ovs_add_port)
    # os.system('ifconfig br0 0.0.0.0/24')
    os.system('ifconfig br0 0')
    os.system('ifconfig ovs-br1 192.168.0.1/24 up')
    os.system('ifconfig ' + eth_port + ' up')

    os.system('ovs-ofctl add-flow ovs-br0 priority=1,in_port=' + eth_port + ',actions=output:ovs-br0-eth1')
    os.system('ovs-ofctl add-flow ovs-br0 priority=1,in_port=ovs-br0-eth1,actions=output:'+ eth_port)
    os.system('ovs-ofctl add-flow ovs-br1 priority=1,in_port=ovs-br1-eth1'',actions=NORMAL')
    os.system('ovs-ofctl add-flow ovs-br1 priority=1,in_port=LOCAL,actions=output:ovs-br1-eth1')
    
    #add flow
    # os.system('nmcli connection show')
    # os.system('ovs-vsctl show')
    # os.system('ryu-manager --verbose --observe-links simple_switch_13_exp.py &') 
    # test

    # ovs-ofctl dump-flows ovs-br0 --protocols=OpenFlow13
    # sudo ip netns exec h1 /bin/bash --rcfile <(echo "PS1=\"namespace h1> \"")
    # sudo ip netns exec h1 ping google.com -c 3


	