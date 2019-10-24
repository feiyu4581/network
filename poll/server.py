# coding:utf-8
import select
import socket
import sys
import queue


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

server_address = ('localhost', 10000)
server.bind(server_address)

server.listen(5)
message_queues = {}

# 传入 poll() 的超时时间(单位是毫秒)
TIMEOUT = 1000

# 使用一个类来实现 poll(),这个类管理着所监视的注册数据通道,通过调用 register() 添加,同时利用标志指示该通道关注那些事件
# POLLIN:输入准备就绪
# POLLPRI:优先级输入准备就绪
# POLLOUT:能够接受输出
# POLLERR:错误
# POLLHUP:通道关闭
# POLLNVAL:通道为打开

READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT

poller = select.poll()
# 注册server的读事件
poller.register(server, READ_ONLY)

# poll()返回一个元组列表(包含套接字的文件描述符和事件),所以为了拿到具体的socket,需要维护一个 套接字的文件描述符 到 socket 的映射
fd_to_socket = {
    server.fileno(): server
}

while True:
    print('Waiting for the next event')
    events = poller.poll()

    for fd, flag in events:
        s = fd_to_socket[fd]

        # 处理读事件
        if flag & (select.POLLIN | select.POLLPRI):
            if s is server:
                connection, client_address = s.accept()
                print('Connection from', client_address)
                connection.setblocking(0)
                fd_to_socket[connection.fileno()] = connection

                poller.register(connection, READ_ONLY)
                message_queues[connection] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    print('Received %s from %s' % (data, s.getpeername()))
                    message_queues[s].put(data)
                    # 将监控写入事件放到当前套接字中
                    poller.modify(s, READ_WRITE)
                else:
                    print('Closing', s.getpeername())
                    del fd_to_socket[s.fileno()]
                    poller.unregister(s)
                    s.close()

                    del message_queues[s]
        # 这里表示一个客户被挂起连接了,这个时候应该主动关闭它
        elif flag & select.POLLHUP:
            print('Closing', s.getpeername())
            del fd_to_socket[s.fileno()]
            poller.unregister()
            s.close()

            del message_queues[s]
        elif flag & select.POLLOUT:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                print(s.getpeername(), 'Queue Empty')
                poller.modify(s, READ_ONLY)
            else:
                print('Sending %s to %s' % (next_msg, s.getpeername()))
                s.send(next_msg)
        elif flag & select.POLLERR:
            print('Exception On', s.getpeername())
            del fd_to_socket[s.fileno()]
            poller.unregister(s)

            s.close()

            del message_queues[s]

