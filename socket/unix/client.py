# coding:utf-8

import socket
import sys

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = './uds_socket'
print('Connecting to %s' % server_address)
try:
    sock.connect(server_address)
except socket.error as msg:
    print (msg)
    sys.exit(1)

try:
    message = 'This is the message. It will be repeated'
    print('Sending', message)
    sock.sendall(message.encode())

    received, expected = 0, len(message)
    while received < expected:
        data = sock.recv(10)
        received += len(data)
        print('Received ', data)
finally:
    sock.close()
