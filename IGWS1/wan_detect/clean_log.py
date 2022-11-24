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



if __name__=='__main__':
    dir = ("/home/pi/IGWS/IGWS1/wan_detect/log/")
    clean_log(dir)
#     size = getdirsize("/home/blacklutos/IGWS/wan_detect/log")
#     print(size)
#     if size > 100:
#         os.system("sudo rm /home/blacklutos/IGWS/wan_detect/log/*.log")