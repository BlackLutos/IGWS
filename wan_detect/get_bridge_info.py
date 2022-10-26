import netifaces as ni

def get_bridge_ip():
    try:
        ip = ni.ifaddresses('br0')[ni.AF_INET][0]['addr']
    except:
        ip = '0.0.0.0'
    # print(ip)  # should print "192.168.0.1"
    ip_info = open('bridge_info','w')
    ip_info.write(ip)
    ip_info.close() 
    return ip
def get_link_info():
    with open('/home/blacklutos/IGWS/wan_detect/link_info.json', 'r') as link_info:
        return link_info.readline()