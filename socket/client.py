# coding:utf-8

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
sock.connect(server_address)

try:
    message = 'Peter'
    print('Sending %s' % message)
    sock.sendall(message.encode())
    received, expected = 0, len(message)
    while received < expected:
        data = sock.recv(16)
        print('Recving', data)
        received += len(data)

finally:
    sock.close()
