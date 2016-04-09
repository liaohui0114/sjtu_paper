#!/usr/bin/env python
# -*- coding:utf-8 -*-

SOCKET_SERVER_IP = '127.0.0.1'
SOCKET_SERVER_PORT = 50000
SOCKET_BUFFER_SIZE = 1024  #packet size of socket(send/receive) 
SOCKET_TIME_OUT = 8
THREAD_NUM = 5
taskQueueDic = {1:"1.png",
           2:"2.jpg",
           3:"3.zip",
           4:"4.tar.gz",
           5:"5.zip",
           6:"6.deb",
           7:"7.tgz",
           8:"8.zip",
           9:"9.mkv",
           10:"10.mkv",}

fileAddrDic = {"1.png":["192.168.3.6","192.168.3.7"],
           "2.jpg":["192.168.3.6","192.168.3.7"],
           "3.zip":["192.168.3.6","192.168.3.7"],
           "4.tar.gz":["192.168.3.6","192.168.3.7"],
           "5.zip":["192.168.3.6","192.168.3.7"],
           "6.deb":["192.168.3.6","192.168.3.7"],
           "7.tgz":["192.168.3.6","192.168.3.7"],
           "8.zip":["192.168.3.6","192.168.3.7"],
           "9.mkv":["192.168.3.6","192.168.3.7"],
           "10.mkv":["192.168.3.6","192.168.3.7"],}

taskingQueueDic = {1:False,
           2:False,
           3:False,
           4:False,
           5:False,
           6:False,
           7:False,
           8:False,
           9:False,
           10:False,}
