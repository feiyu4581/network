# coding: utf-8

import select
import socket
import queue

server_address = ('localhost', 10000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)

server.bind(server_address)
server.listen(5)

# 可以使用 添加一个 select.EPOLLET 来使用 边缘触发,此时相关的连接的活动只会触发一次
READ_ONLY = select.EPOLLIN | select.EPOLLPRI | select.EPOLLERR | select.EPOLLHUP
READ_WRITE = READ_ONLY | select.EPOLLOUT
message_queues = {}
fd_to_socket = {server.fileno(): server}

epoll = select.epoll()
epoll.register(server, READ_ONLY)

while True:
    print('Waiting the next event')
    events = epoll.poll()
    for fd, flag in events:
        sock = fd_to_socket[fd]

        if flag & (select.EPOLLIN | select.EPOLLPRI):
            if sock is server:
                connection, client_address = sock.accept()
                connection.setblocking(0)
                print('Connection from', client_address)

                epoll.register(connection, READ_ONLY)
                fd_to_socket[connection.fileno()] = connection
                message_queues[connection] = queue.Queue()
            else:
                data = sock.recv(1024)
                if data:
                    print('Receiving data %s from %s' % (data, sock.getpeername()))
                    message_queues[sock].put(data)
                    epoll.modify(sock, READ_WRITE)
                else:
                    print('Client close from', sock.getpeername())
                    epoll.unregister(sock)
                    sock.close()

                    del message_queues[sock]
                    del fd_to_socket[fd]
        elif flag & select.EPOLLERR:
            print('Error happend from', sock.getpeername())
            epoll.unregister(sock)
            sock.close()
            
            del message_queues[sock]
            del fd_to_socket[fd]
        elif flag & select.EPOLLHUP:
            print('HUP happed from', sock.getpeername())
            epoll.unregister(sock)
            sock.close()

            del message_queues[sock]
            del fd_to_socket[fd]
        elif flag & select.EPOLLOUT:
            try:
                next_msg = message_queues[sock].get_nowait()
            except queue.Empty:
                print('Message Empty', sock.getpeername())
                epoll.modify(sock, READ_ONLY)
            else:
                print('Sending %s to %s' % (next_msg, sock.getpeername()))
                sock.send(next_msg)
