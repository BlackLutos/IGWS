f = open('log/timestamp/timestamp.txt','r')
timestamp = f.read()
f.close()
f = open('log/' + timestamp ,'r')
wan_state = f.read()
f.close()
print(timestamp + ":" + wan_state)
if "Normal" in wan_state:
    print('Normal! Don\'t need to notice to controller.')
else:
    print('Abnormal! Notice to controller.')