#!/usr/bin/python 
#coding:utf-8 
import sys,os
import socket, time

if __name__ == '__main__':
#     for arg in sys.argv:
#         print arg
    #serverip = '127.0.0.1'
    #serverport = 55555
    serverip = sys.argv[1]
    serverport = int(sys.argv[2])
    m_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #define socket,using TCP protocol
    print 'start connection to server'
   # m_socket.settimeout(5) #set timeout == 5
    m_socket.connect((serverip,serverport))#connect server
    print 'connection success,send msg:hello'
    m_socket.send("hello")
    data = m_socket.recv(1024)
    print data
    m_socket.close()
         
    
