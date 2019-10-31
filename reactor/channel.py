# coding:utf-8
from reactor.const import READ, WRITE, HUP, ERROR, EVENT_READ


class Channel(object):
    def __init__(self, server):
        self.server = server
        self.fd = server.fileno()
        self.events = EVENT_READ

    def on_server_ready(self, event_loop):
        pass

    def on_write(self, event_loop):
        pass

    def on_hup(self, event_loop):
        pass

    def on_error(self, event_loop):
        pass

    def handle_callback(self, event_loop, event):
        if event & READ:
            self.on_server_ready(event_loop)
        elif event & WRITE:
            self.on_write(event_loop)
        elif event & HUP:
            self.on_hup(event_loop)
        elif event & ERROR:
            self.on_error(event_loop)
