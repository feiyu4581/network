# coding:utf-8
import sys
import os

sys.path.append('/home/zhuzx/github/network')
from reactor.event_loop import EventLoop


def on_message(message):
    print('On Message', message)
    return message


server_address = ('localhost', 10000)

event_loop = EventLoop(server_address)
event_loop.activate_sub_work(on_message, nums=4)
event_loop.run()
