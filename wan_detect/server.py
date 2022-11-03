import select
import socket
import json
import os

def start_server(port):
    HOST = '0.0.0.0'
    PORT = port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))   
    server.listen(10)           

    inputs = [server]           
    outputs = []                

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        # 可读
        for s in readable:
            if s is server:     
                connection, client_address = s.accept()
                inputs.append(connection)
            else:
                data = s.recv(1024)        
                if data:
                   
                    print(data.decode(encoding='utf-8'))
                    info = data.decode(encoding='utf-8')
                    failover_flag = False
                    print('-------------------------------')
                    # with open('config.json','r') as f:
                    #     config = json.load(f)
                    # if (('Wan_State:Abnormal' in info) & (config['wan_state'] == 'Abnormal')):
                    #     info = info.split(',',4)
                    #     wan_state = (info[0].split(':',1))[1]
                    #     bridge_ip = (info[1].split(' ',3))[3]
                    #     with open('config.json','r') as f:
                    #         config = json.load(f)
                    #     config['wan_state'] = 'Failover' 
                    #     with open('config.json','w') as f:
                    #         f.write(json.dumps(config))
                    #     failover()
                    if ('Wan_State:Abnormal' in info):
                        failover_flag = True
                    elif ('Wan_State:Failover' in info):
                        os.system('sh add_flow.sh')
                        # print('Failover')


                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    print(inputs)
                    s.close()

        
        for w in writable:
            if failover_flag:
                w.send('Server received data: To do Failover'.encode(encoding='utf-8'))
            else:
                w.send('Server received data: Normal'.encode(encoding='utf-8'))
            outputs.remove(w)

        
        # for s in exceptional:
        #     inputs.remove(s)
        #     if s in outputs:
        #         outputs.remove(s)
        #     s.close()

if __name__ == '__main__':
    start_server(8848)