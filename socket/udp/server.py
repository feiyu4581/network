# coding:utf-8

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
sock.bind(server_address)

print ('Start Server')
while True:
    print('Wainting to receive message')
    data, address = sock.recvfrom(4096)
    print('received %s bytes from %s' % (len(data), address))
    print(data)
    if data:
        sent = sock.sendto(data, address)
        print('sent %s bytes back to %s' % (sent, address))
