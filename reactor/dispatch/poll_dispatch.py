# coding:utf-8

import select
from reactor.dispatch.base import BaseDispatch


class PollDispatch(BaseDispatch):
    def __init__(self, timeout=1):
        self.poller = select.poll()
        self.fd_to_channel = {}
        self.timeout = timeout

    def add(self, channel):
        self.fd_to_channel[channel.fd] = channel
        self.poller.register(channel.server, channel.events)

    def update(self, channel):
        self.fd_to_channel[channel.fd] = channel
        self.poller.modify(channel.server, channel.events)

    def delete(self, channel):
        del self.fd_to_channel[channel.fd]
        self.poller.unregister(channel.server)

    def dispatch(self):
        for fd, flag in self.poller.poll(self.timeout):
            yield self.fd_to_channel[fd], flag

