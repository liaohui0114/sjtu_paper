#!/usr/bin/python 
#coding:utf-8 
import sys,os,json
import socket, time
import threading
import random
import Queue
from variable import *


taskQueue = Queue.Queue(0)
taskCounter = 1




class MonitorClient:   
  
    def __init__(self,server_ip=SOCKET_SERVER_IP,server_port=SOCKET_SERVER_PORT):   
        print 'Prepare for connecting...,ip:%s'%(server_ip)
        self.server_ip = server_ip
        self.server_port = server_port
  
    def connect(self):
        self.start_time = time.time() # timestamp when download start
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.sock.connect((self.server_ip,self.server_port))   
        print 'connected'
        return True

    def getMonitorInfo(self):
        
        self.sock.sendall('monitor:%s'%(self.server_ip)) #send file_name to server and waiting for data
        data = self.sock.recv(1024)

        
        monitorinfo = {}
        #data not None
        if data:
            monitorinfo = json.loads(data)  

        self.sock.close()
            
        return monitorinfo


def monitorThread(serverip=SOCKET_SERVER_IP):
    print '###################start get monitor thread,ip=%s'%(serverip)
    info = {KEY_NET_SEND:sys.maxint,KEY_NET_RECV:sys.maxint,KEY_NET_DELAY:sys.maxint}

    try:
        client = MonitorClient(server_ip=serverip)

        if client.connect():
            #print "filename:"+file_name
            start_time = time.time() 
            monitorinfo = client.getMonitorInfo()
            end_time = time.time()
            if monitorinfo:
                info[KEY_NET_SEND] = monitorinfo[KEY_NET_SEND]
                info[KEY_NET_RECV] = monitorinfo[KEY_NET_RECV]
                info[KEY_NET_DELAY] = end_time - start_time
            print '######monitor_info=%s,ip=%s'%(info,serverip)
        
    except:
        print 'eee:except'   
    
    f = open("../log/monitorinfo-%s.txt"%(serverip),"a") #########################
    mi = "%s\t%s\t%s\t%s\n"%(info[KEY_NET_SEND],info[KEY_NET_RECV],info[KEY_NET_DELAY],start_time)
    f.write(mi)
    f.flush()
    f.close()    
    print '###################finish monitor thread,ip=%s'%(serverip)

if __name__ == '__main__':
    #initial threads
    ip_list = addr_list[0:ERASURE_CODE_N]
    while True:
        thread_list = []
        for index,ipaddr in enumerate(ip_list):
            thread_list.append(threading.Thread(target=monitorThread,args=(ipaddr,)))
        for item in thread_list:
            item.start()
        for item in thread_list:
            item.join()
        time.sleep(0.5)
     

         
    

