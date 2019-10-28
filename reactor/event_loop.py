# coding:utf-8
from reactor.const import CHANNEL_ADD, CHANNEL_DEL, CHANNEL_UPDATE


class EventLoop(object):
    def __init__(self, dispatch, name='Main Thread'):
        self.dispatch = dispatch
        self.name = name
        self.waiting_channels = []
        self.work_nums = 0
        self.works = []

    def handle_waiting_channels(self):
        for channel, event in self.waiting_channels:
            if event == CHANNEL_ADD:
                self.dispatch.add(channel)
            elif event == CHANNEL_UPDATE:
                self.dispatch.update(channel)
            elif event == CHANNEL_DEL:
                self.dispatch.delete(channel)

    def run(self):
        while True:
            self.handle_waiting_channels()
            for channel, event in self.dispatch.dispatch():
                channel.handle_callback(self, event)

    def add_channel(self, channel):
        self.waiting_channels.append((channel, CHANNEL_ADD))

    def del_channel(self, channel):
        self.waiting_channels.append((channel, CHANNEL_DEL))

    def update_channel(self, channel):
        self.waiting_channels.append((channel, CHANNEL_UPDATE))

    def activate_sub_work(self, channel, work_num):
        pass
