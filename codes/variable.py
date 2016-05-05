#!/usr/bin/env python
# -*- coding:utf-8 -*-

SOCKET_SERVER_IP = '127.0.0.1'
SOCKET_SERVER_PORT = 50000
SOCKET_BUFFER_SIZE = 1024  #packet size of socket(send/receive) 
SOCKET_TIME_OUT = 8
THREAD_NUM = 5
TASK_NUMBER = 40

ERASURE_CODE = 2

KEY_NET_SEND = 'key_net_send'
KEY_NET_RECV = 'key_net_recv'
KEY_NET_DELAY = 'key_net_delay'
taskQueueDic = {0:"0.png",
           1:"1.jpg",
           2:"2.zip",
           3:"3.zip",
           4:"4.tar.gz",
           5:"5.zip",
           6:"6.deb",
           7:"7.tgz",
           8:"8.mkv",
           9:"9.mkv",}

addr_list = ["192.168.3.6","192.168.3.7","192.168.3.8"]
'''
addr_list = ["127.0.0.1"]
'''

fileAddrDic = {"0.png":["192.168.3.6","192.168.3.7","192.168.3.8"],
           "1.jpg":["192.168.3.6","192.168.3.7","192.168.3.8"],
           "2.zip":["192.168.3.6","192.168.3.7","192.168.3.8"],
           "3.zip":["192.168.3.6","192.168.3.7","192.168.3.8"],
           "4.tar.gz":["192.168.3.6","192.168.3.7","192.168.3.8"],
           "5.zip":["192.168.3.6","192.168.3.7","192.168.3.8"],
           "6.deb":["192.168.3.6","192.168.3.7","192.168.3.8"],
           "7.tgz":["192.168.3.6","192.168.3.7","192.168.3.8"],
           "8.mkv":["192.168.3.6","192.168.3.7","192.168.3.8"],
           "9.mkv":["192.168.3.6","192.168.3.7","192.168.3.8",],}
'''

fileAddrDic = {"0.png":["127.0.0.1",],
           "1.jpg":["127.0.0.1",],
           "2.zip":["127.0.0.1",],
           "3.zip":["127.0.0.1",],
           "4.tar.gz":["127.0.0.1",],
           "5.zip":["127.0.0.1",],
           "6.deb":["127.0.0.1",],
           "7.tgz":["127.0.0.1",],
           "8.mkv":["127.0.0.1",],
           "9.mkv":["127.0.0.1",],}

'''
taskingQueueDic = {0:False,
           1:False,
           2:False,
           3:False,
           4:False,
           5:False,
           6:False,
           7:False,
           8:False,
           9:False,}
