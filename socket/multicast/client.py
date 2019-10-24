# coding:utf-8

import socket
import struct

multicast_group = '224.3.29.71'
server_address = ('', 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

# 使用 setsockopt 将当前 sock 添加到组里面,使用 INADDR_ANY 监听所有端口
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    print('Waiting to receive message')
    data, address = sock.recvfrom(1024)
    print('Received %s bytes from %s' % (len(data), address))
    print (data)

    sock.sendto(b'ack', address)
