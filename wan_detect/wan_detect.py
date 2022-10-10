from ping3 import ping
import logging
import time
from datetime import timedelta
import datetime
from datetime import datetime
from datetime import date
import os
from os.path import join, getsize

def getdirsize(dir):
    size = 0
    for path,dirs,files in os.walk(dir):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
        return size
def clean_log(dir):
    files = []
    for file in os.listdir(dir):
        files.append(file)
    files.remove('timestamp')
    files.remove('detail')
    files.sort()
    files_num = len(files)
    size = getdirsize(dir)
    for i in range(files_num // 2):
        if size > 100:
            os.remove(dir + files[i])

dir = ("/home/blacklutos/IGWS/wan_detect/log/")
# f = open('/home/blacklutos/IGWS/wan_detect/interval.txt','r')
# interval_time = int(f.read())
# f.close()
# now_time = datetime.now() + timedelta(hours=8)
os.system('sudo timedatectl set-timezone Asia/Taipei')

while True:
    now_time = datetime.now()
    now_time = now_time.strftime("%Y-%m-%d %H-%M-%S")
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.INFO, filename = "/home/blacklutos/IGWS/wan_detect/log/detail/wan_state.log", filemode='a' ,format=FORMAT)
    log_file = open("/home/blacklutos/IGWS/wan_detect/log/wan_state_" + now_time + ".log",'w')

    wan_state = ping('google.com',timeout=10)
    if wan_state:
        logging.info("Normal")
        log_file.write("Normal")
    else:
        logging.info("Abnormal")
        log_file.write("Abnormal")
    log_file.close()
    clean_log(dir)
    

    f = open('/home/blacklutos/IGWS/wan_detect/log/timestamp/timestamp.txt','w')
    f.write("wan_state_" + now_time + ".log")
    f.close()

    f = open('/home/blacklutos/IGWS/wan_detect/interval.txt','r')
    interval_time = int(f.read())
    f.close()
    time.sleep(interval_time)