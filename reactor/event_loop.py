# coding:utf-8
from reactor.const import CHANNEL_ADD, CHANNEL_DEL, CHANNEL_UPDATE
from reactor.dispatch.poll_dispatch import PollDispatch
from reactor.main_thread import AccepterChannel, WeakupChannel
import threading
import socket


def sub_work(parent, num):
    child_loop = EventLoop(name='Thread {}'.format(num), main_thread=False)
    parent_fd, child_fd = socket.socketpair()
    child_loop.weak_server = parent_fd
    child_loop.add_channel(WeakupChannel(child_fd))

    parent.add_child(child_loop)

    with parent.cond:
        parent.cond.notifyAll()

    child_loop.run()


class EventLoop(object):
    def __init__(self, server_address=None, name='Main Thread', main_thread=True):
        self.dispatch = PollDispatch()
        self.main_thread = main_thread
        self.server_address = server_address
        self.name = name
        self.waiting_channels = []
        self.work_nums = 0
        self.works = []
        self.position = 0
        self.weak_server = None

        self.lock = threading.Lock()
        self.cond = threading.Condition()

        self.on_message = None
    
    def add_child(self, child_loop):
        with self.lock:
            self.works.append(child_loop)

    def add_child_channel(self, channel):
        if self.position >= len(self.works):
            self.position = 0

        self.works[self.position].add_channel(channel)
        self.works[self.position].weak_server.send(b'weak')
        self.position += 1

    def handle_waiting_channels(self):
        for channel, event in self.waiting_channels:
            if event == CHANNEL_ADD:
                self.dispatch.add(channel)
            elif event == CHANNEL_UPDATE:
                self.dispatch.update(channel)
            elif event == CHANNEL_DEL:
                self.dispatch.delete(channel)

        self.waiting_channels = []

    def run(self):
        if self.main_thread:
            self.add_main_channel()

        while True:
            self.handle_waiting_channels()
            for channel, event in self.dispatch.dispatch():
                channel.handle_callback(self, event)

    def add_channel(self, channel):
        with self.lock:
            self.waiting_channels.append((channel, CHANNEL_ADD))

    def del_channel(self, channel):
        with self.lock:
            self.waiting_channels.append((channel, CHANNEL_DEL))

    def update_channel(self, channel):
        with self.lock:
            self.waiting_channels.append((channel, CHANNEL_UPDATE))

    def add_main_channel(self):
        self.add_channel(AccepterChannel(self.server_address))

    def activate_sub_work(self, on_messge, nums=4):
        self.on_message = on_messge
        self.work_nums = nums

        for num in range(nums):
            with self.cond:
                sub = threading.Thread(target=sub_work, args=(self, num))
                sub.start()

                self.cond.wait()
