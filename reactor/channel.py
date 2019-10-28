# coding:utf-8

class Channel(object):
    def __init__(self, connection, events):
        self.connection = connection
        self.events = events
        self.on_read = None
        self.on_write = None
        self.on_close = None
        self.on_error = None

    def handle_callback(self, event_loop, event):
        pass
