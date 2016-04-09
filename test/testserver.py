#!/usr/bin/python 
#coding:utf-8 
import sys,os
import socket, time

  
if __name__ == '__main__':
#     serverip = '127.0.0.1'
#     serverport = 55555
    serverip = sys.argv[1]
    serverport = int(sys.argv[2])
    m_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #define socket,using TCP protocol            
    m_socket.bind((serverip,serverport)) #bind ip and port
    m_socket.listen(1) #set client num that can connect the server at same time
    while True:
        conn,addr = m_socket.accept()
        data = conn.recv(1024)
        print 'data from client:%s'%(data)
        conn.send('ok!')
        conn.close()