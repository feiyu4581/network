# coding:utf-8
import socket
from reactor.sub_thread import MessageChannel
from reactor.channel import Channel


class AccepterChannel(Channel):
    def __init__(self, server_address):
        self.server_address = server_address
        super(AccepterChannel, self).__init__(self.activate_server())

    def activate_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setblocking(0)
        server.bind(self.server_address)
        server.listen(1024)

        return server

    def on_server_ready(self, event_loop):
        connection, client_address = self.server.accept()
        connection.setblocking(0)
        event_loop.add_child_channel(MessageChannel(connection, client_address))


class WeakupChannel(Channel):
    def on_server_ready(self, event_loop):
        try:
            print('Weak: %s' % self.server.recv(8))
        except Exception:
            pass
