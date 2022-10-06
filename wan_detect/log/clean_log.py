import os
from os.path import join, getsize

def getdirsize(dir):
    size = 0
    for path,dirs,files in os.walk(dir):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
        return size



if __name__=='__main__':
    size = getdirsize("/home/blacklutos/IGWS/wan_detect/log")
    print(size)
    if size > 1000:
        os.system("sudo rm *.log")