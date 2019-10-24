# coding:utf-8

import socket
import sys

messages = [
    b'This is the message',
    b'It will be sent',
    b'In Parts.'
]

server_address = ('localhost', 10000)
socks = [
    socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for _ in range(20)
]

print('Connecting to %s port %s' % server_address)
for s in socks:
    s.connect(server_address)

for message in messages:
    for s in socks:
        print('%s: sending %s' % (s.getsockname(), message))

        s.send(message)

    for s in socks:
        data = s.recv(1024)
        print('%s: Received %s' % (s.getsockname(), data))
        
        if not data:
            print('Closing socket', s.getsockname())
            s.close(0)
