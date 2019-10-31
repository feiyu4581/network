# coding:utf-8
import select

CHANNEL_ADD = 'add'
CHANNEL_UPDATE = 'update'
CHANNEL_DEL = 'delete'


READ = select.EPOLLIN | select.EPOLLPRI
WRITE = select.EPOLLOUT
HUP = select.EPOLLHUP
ERROR = select.EPOLLERR

EVENT_READ = READ | HUP | ERROR
EVENT_WRITE = EVENT_READ | WRITE
