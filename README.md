# IGWS For internship in [O’PRUEBA](https://www.oprueba.com/)
<img width="451" alt="image" src="https://user-images.githubusercontent.com/8721804/203735502-8222cb7d-05b5-41ba-bb5d-d8d15ae3e2ed.png">
<img width="541" alt="image" src="https://user-images.githubusercontent.com/8721804/203735372-ba2b807b-a8d5-4376-ade7-b4c9c293938a.png">

### Streamlined SOP for testing
``
sudo python3 create.py ==> cd wan_detect ==> change the value of config.json ==> sudo python3 server.py ==> sudo python3 client.py
``
### The following are the details ↓

### Create Topology & Envirment
[create.py](https://github.com/BlackLutos/IGWS/blob/main/create.py)
```
$ sudo python3 create.py
```
### Delete Topology & Envirment
[delete.py](https://github.com/BlackLutos/IGWS/blob/main/delete.py)
```
$ sudo python3 delete.py
```
### Enable Controller
[controller.py](https://github.com/BlackLutos/IGWS/blob/main/controller.py)
```
$ sudo ryu-manager --observe-links controller.py
```

## Wan Detection
### Change to directory
```
$ cd wan_detect 
```

### Enable Wan Detect Service (If you just want to test, don't need to enable the service. the log timestamp default is abnormal status.)
[service_wan_detect.sh](https://github.com/BlackLutos/IGWS/blob/main/wan_detect/service_wan_detect.sh)
```
$ sudo bash service_wan_detect.sh
```
#### Stop & Restart Service
[stop_service.sh](https://github.com/BlackLutos/IGWS/blob/main/wan_detect/stop_service.sh)
[start_service.sh](https://github.com/BlackLutos/IGWS/blob/main/wan_detect/start_service.sh)
##### Stop service
```
$ sudo bash stop_service.sh
```
##### Restart service
```
$ sudo bash start_service.sh
```
### Socket controller Clinet & Server
##### Before testing the methods, need to change the value of [config.json](https://github.com/BlackLutos/IGWS/blob/main/wan_detect/config.json).
``
config.json: {"wan_state": "Failover"} ==> {"wan_state": "Abnormal"}
``
##### Client & Server
[client.py](https://github.com/BlackLutos/IGWS/blob/main/wan_detect/client.py)
[server.py](https://github.com/BlackLutos/IGWS/blob/main/wan_detect/server.py)
##### Need to enable server first and then enable client. (Recommend at least 2 split screens.)
```
$ sudo python3 server.py
$ sudo python3 client.py
```

