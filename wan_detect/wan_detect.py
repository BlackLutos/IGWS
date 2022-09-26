from ping3 import ping
import logging
import time
from datetime import timedelta
import datetime
from datetime import datetime
from datetime import date

f = open('/home/blacklutos/IGWS/wan_detect/interval.txt','r')
interval_time = int(f.read())
f.close()
now_time = datetime.now() + timedelta(hours=8)
now_time = now_time.strftime("%Y-%m-%d %H-%M-%S")
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename = "/home/blacklutos/IGWS/wan_detect/log/wan_state_" + now_time + ".log", filemode='w')

wan_state = ping('google.com')
if wan_state:
    logging.info("Normal")
else:
    logging.info("Abnormal")

f = open('/home/blacklutos/IGWS/wan_detect/log/timestamp/timestamp.txt','w')
f.write("wan_state_" + now_time + ".log")
f.close()
time.sleep(interval_time)