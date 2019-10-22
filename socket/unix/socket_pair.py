# coding:utf-8
import socket
import os

parent, child = socket.socketpair()

pid = os.fork()
if pid:
    print('In Parent, sending message')
    child.close()
    parent.sendall(b'ping')
    response = parent.recv(1024)
    print('Response from child:', response)
    parent.close()
else:
    print('In Child, waiting for message')
    parent.close()
    message = child.recv(1024)
    print('Message from parent:', message)
    child.sendall(b'pong')
    child.close()
