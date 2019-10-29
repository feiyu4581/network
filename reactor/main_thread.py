# coding:utf-8
import socket

class AccepterChannel(object):
    def __init__(self, server_address):
        self.server_address = server_address
        self.activate_server()

    def activate_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setblocking(0)
        server.bind(self.server_address)
        server.listen(1024)

        self.server = server

    def on_server_ready(self):
        pass


class AccepterHandler(object):
    pass
