# coding:utf-8

import socket
import struct
import os

# 使用组播(multicast)会向多个端点同时发送消息
# 使用 UDP 发送,向一个组播组(multicast group),这是一个常规的 IPv4 地址范围的一个子集(224.0.0.0 到 230.255.255.255)
# 这些地址会由网络路由器和交换机特殊处理,所有发送到这个组的的消息可以在互联网上分发到加入这个组的所有接收方

message = 'Very Import Data'
multicast_group = ('224.3.29.71', 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 设置超时时间
sock.settimeout(0.2)

# 设置 TTL 值(这个值表示消息允许经过多少次网络中路由器的跳转, 需要包装为一个字节)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:
    print('Sending', message)
    sent = sock.sendto(message.encode(), multicast_group)

    while True:
        print('Waiting to receive')
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('Timeout')
            break
        else:
            print('Received %s from %s' % (data, server))
finally:
    sock.close()
