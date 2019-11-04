# coding:utf-8
import socket
import queue
from reactor.const import EVENT_READ, EVENT_WRITE
from reactor.channel import Channel


class MessageChannel(Channel):
    def __init__(self, connection, client_address):
        super(MessageChannel, self).__init__(connection)

        self.client_address = client_address
        self.send_buffers = queue.Queue()

    def on_server_ready(self, event_loop):
        datas = b''
        while True:
            try:
                data = self.server.recv(1024)
            except socket.error:
                break
            else:
                if data:
                    datas += data
                else:
                    return event_loop.del_channel(self)

        if datas:
            self.send_buffers.put('Send: %s\n' % (datas))
            self.events = EVENT_WRITE
            event_loop.update_channel(self)
            print('Receive Datas %s from %s' % (datas, self.client_address))

    def on_write(self, event_loop):
        try:
            msg = self.send_buffers.get_nowait()
        except queue.Empty:
            self.events = EVENT_READ
            event_loop.update_channel(self)
        else:
            print('[%s]Send Datas %s' % (event_loop.name, msg))
            self.server.send(msg.encode())
