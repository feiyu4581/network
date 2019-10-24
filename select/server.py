# coding:utf-8
import select
import socket
import sys
import queue

# 创建一个 TCP/IP 的socket,并设置为 非阻塞
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

server_address = ('localhost', 10000)
print('Starting Server...')

server.bind(server_address)
server.listen(5)

inputs = [ server ]
outputs = []

# 填充每个套接字将要发送的消息
message_queues = {}
while inputs:
    print('Waitint for the next version')

    # select 需要三个参数, 其中
    # 第一个对象列表里面是需要监控读取的文件句柄
    # 第二个对象列表里面是需要监控写入的文件句柄
    # 第三个对象列表里面是需要监控会发生错误的句柄(通常是 inputs 和 outputs 的全部对象)
    # select 接受第四个可选参数,表示超时时间(单位是 秒), 这个时候可以判断返回列表为空来做一些额外的事情

    # 同样返回三个新的列表,是所传入列表的子集,表示可控操作的文件句柄集合
    # timeout = 1
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # 处理读取列表
    for s in readable:
        # 判断是否是新的连接到来
        if s is server:
            connection, client_address = s.accept()
            print('Connection from', client_address)
            # 设置为非阻塞
            connection.setblocking(0)
            # 将这个连接加入要读取的列表里面
            inputs.append(connection)

            # 初始化这个套接字的消息列表
            message_queues[connection] = queue.Queue()
        # 如果不是新的连接到来,那么表示有连接数据已经准备好了
        else:
            data = s.recv(1024)
            if data:
                print('Receivd %s from %s' % (data, s.getpeername()))
                message_queues[s].put(data)

                # 将当前连接加入到写入列表里面
                if s not in outputs:
                    outputs.append(s)
            else:
                print('Closing ', s.getpeername())

                # 去掉监控这个套接字的读写操作
                if s in outputs:
                    outputs.remove(s)

                inputs.remove(s)
                s.close()

                del message_queues[s]

    # 处理写入列表
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            print(s.getpeername(), 'Queue empty')
            outputs.remove(s)
        else:
            print('Sending %s to %s' % (next_msg, s.getpeername()))
            s.send(next_msg)

    # 处理异常连接
    for s in exceptional:
        print('Exception condition on', s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)

        s.close()

        del message_queues[s]
