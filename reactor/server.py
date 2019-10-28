# coding:utf-8
from reactor.dispatch.poll_dispatch import PollDispatch
from reactor.event_loop import EventLoop
from reactor.main_thread import AccepterChannel, AccepterHandler
from reactor.sub_thread import MessageChannel

server_address = ('localhost', 10000)

event_loop = EventLoop(PollDispatch())
accepter = AccepterChannel().create_main_accepter()

event_loop.add_channel(accepter)
event_loop.activate_sub_work(MessageChannel, 4)

event_loop.run()
