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



# TODO
# 1. server 似乎没有正确的派发的线程中去,都是 server 0
# 2. client 最后一个 read 报错
# 3. 解决每个线程都需要等待超时后才能添加 event 的问题