import glob
data = glob.glob(r"/etc/NetworkManager/system-connections/*")

# br_port = []
# for i in data:
#     br_port.append(i.split('/etc/NetworkManager/system-connections/')[1])
# br_port.remove('br0')
# print(br_port)

x = True

while(x):
    n = input()
    if n == '1':
        print('continute')
    else:
        x = False