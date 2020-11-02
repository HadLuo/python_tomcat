# server.py
# -*- coding=utf-8 -*-
import socket
import threading, queue
from tomcat.core import *


class SocketInfo:
    def __init__(self, socket_, addr):
        self.socket_ = socket_
        self.addr = addr

    def get_socket(self):
        return self.socket_

    def get_addr(self):
        return self.addr


class SocketAcceptor:
    def __init__(self):
        self.running = True
        self.queue = queue.Queue()  # 创建一个队列
        # 数据处理器
        self.handler = HttpHandler()
        # 开启消费者线程
        self.consumer_thread = threading.Thread(target=self.consumer)
        self.consumer_thread.start()
        Log.i("负责处理socket连接的连接器初始化完成！")

    def consumer(self):
        while self.running:
            # 消費到消息
            socket_info = self.queue.get()
            Log.i("client socket connect >> " + str(socket_info.get_addr()))
            self.handler.handle(socket_info)

    def accept_socket(self, socket_info):
        self.queue.put(socket_info)


class ServerSockets:
    def __init__(self, port=8080):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', port))
        # 指定在拒绝连接之前，操作系统可以挂起的最大连接数量
        self.server_socket.listen(255)
        # 链接器
        self.acceptor = SocketAcceptor()
        Log.i("HadLuo-Python-Tomcat start ok！  listen port :" + str(port))

    def startup(self):
        while True:
            # 有客户端连接就返回
            client_sock, addr = self.server_socket.accept()
            # 交給連接器
            self.acceptor.accept_socket(SocketInfo(client_sock, addr))
