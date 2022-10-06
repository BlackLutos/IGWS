import os
import time
import socket
from monitor_wan_state import get_wan_state
from get_bridge_info import get_bridge_ip
from get_bridge_info import get_link_info

def start_client(addr, port):
    PLC_ADDR = addr
    PLC_PORT = port
    s = socket.socket()
    s.connect((PLC_ADDR, PLC_PORT))
    count = 0
    pid = str(os.getpid())
    while True:
        if get_wan_state() == True:
            msg = 'Wan_State:Normal' + ", pid: " + pid
        else:
            bridge_ip = get_bridge_ip()
            link_info = get_link_info()
            msg = 'Wan_State:Abnormal, ' + 'bridge IP: ' + bridge_ip + ', link_info: ' + link_info + ", pid: " + pid

        msg = msg.encode(encoding='utf-8')
        s.send(msg)
        recv_data = s.recv(1024)
        print(recv_data.decode(encoding='utf-8'))
        time.sleep(3)
        # count += 1
        # if count > 2000:
        #     break

    s.close()

if __name__ == '__main__':
    start_client('127.0.0.1', 8801)