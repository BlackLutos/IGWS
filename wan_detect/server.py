import select
import socket


def start_server(port):
    HOST = '0.0.0.0'
    PORT = port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))   # 套接字绑定的IP与端口
    server.listen(10)           # 开始TCP监听

    inputs = [server]           # 存放需要被检测可读的socket
    outputs = []                # 存放需要被检测可写的socket

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        # 可读
        for s in readable:
            if s is server:     # 可读的是server,说明有连接进入
                connection, client_address = s.accept()
                inputs.append(connection)
            else:
                data = s.recv(1024)        # 故意设置的这么小
                if data:
                    # 已经从这个socket当中收到数据, 如果你想写, 那么就将其加入到outputs中, 等到select模型检查它是否可写
                    print(data.decode(encoding='utf-8'))
                    if s not in outputs:
                        outputs.append(s)
                else:
                    # 收到为空的数据,意味着对方已经断开连接,需要做清理工作
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

        # 可写
        for w in writable:
            w.send('Server received data'.encode(encoding='utf-8'))
            outputs.remove(w)

        # 异常
        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()

if __name__ == '__main__':
    start_server(8801)