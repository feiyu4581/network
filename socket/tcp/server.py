# coding:utf-8

import socket
import sys

# socket.AF_INET: ipv4
# socket.AF_INET6: ipv6
# socket.AF_UNIX: Unix 域

# socket.SOCK_STREAM: 传输控制协议(TCP)
# socket.SOCK_DGRAM: 用户数据报协议(UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
sock.bind(server_address)

# 将这个套接字设置为服务器模式,等待后续的连接,参数表示后台排队的连接数,超过这个连接数后,系统会拒绝新客户
sock.listen(1)

while True:
    print ('waiting for a connection')
    connection, client_address = sock.accept()
    # 这里设为 0 的时候采用非阻塞IO
    connection.setblocking(0)
    try:
        print ('connection from', client_address)
        while True:
            print ('Start Recv')
            try:
                data = connection.recv(16)
            except socket.error as e:
                print (e)
                continue
            print ('Recevid %r' % data)
            if data:
                connection.sendall(data)
            else:
                print ('no data from', client_address)
                break
    finally:
        connection.close()
