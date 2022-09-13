import sh
import os
import time
print('creating...')
sh.bash('create_linux_bridge.sh')
sh.bash('ovs_create.sh')
# os.system('cat ping_result.log')
# os.system('brctl show')
os.system('nmcli connection show')
os.system('ovs-vsctl show')
os.system('ip netns exec h1 ifconfig')
print('Finish !!!')
#topology graph
