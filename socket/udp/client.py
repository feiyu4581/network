# coding: utf-8

import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)

message = 'This is a message, It will be repeated'
try:
    print('sending ', message)
    sent = sock.sendto(message.encode(), server_address)
    print('Waiting to receive')
    data, server = sock.recvfrom(4096)
    print('received ', data)
finally:
    sock.close()
