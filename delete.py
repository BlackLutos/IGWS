import os
import sh

print('deleting...')
sh.bash('delete_linux_bridge.sh')
sh.bash('ovs_delete.sh')
os.system('nmcli connection show')
os.system('ovs-vsctl show')
sh.mn('-c')
print('Finish !!!')