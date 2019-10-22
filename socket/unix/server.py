# coding:utf-8

import socket
import os
import sys

server_address = './uds_socket'

try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind(server_address)

sock.listen(1)

while True:
    print('Waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('Connection from', client_address)
        while True:
            data = connection.recv(16)
            print ('Received', data)
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()
