#!/usr/bin/python 
#coding:utf-8 
import sys,os
import socket, time
import threading
import random
import Queue
from variable import *


taskQueue = Queue.Queue()
taskCounter = 1

######################scheduler####################################################
#erasure code:(n,k) = (Erasure_code_n,erasure_code,k)
def monitorScheduler(ip_list,isScheduled = False):
    #print 'ip_list,11111111111',ip_list
    ip_list = ip_list[0:ERASURE_CODE_N]
    #print 'ip_list,22222222222',ip_list
    if not isScheduled:
        return random.sample(ip_list,ERASURE_CODE_K) #return random erasure_code_num's ip from ip_list

    #scheduling
    monitor_dict = {}
    for ipaddr in ip_list:
        f = open("../log/monitorinfo-%s.txt"%(ipaddr),"r") #########################
        last_line = f.readlines()[-1]
        f.close()
        monitor_info = last_line.split()
        monitor_dict[ipaddr] = monitor_info
    #print monitor_dict

    ##d[1][0]:by net_send;d[1][1]:by_recv;2:by delay
    tmp_ip_list = sorted(monitor_dict.items(),key=lambda d:d[1][0]) #sorted by value[0](d[0]:key,d[1]:values) by ascend
    #print tmp_ip_list
    rtn_ip_list = []
    for i in xrange(0,ERASURE_CODE_K):
        rtn_ip_list.append(tmp_ip_list[i][0])
    #print 'ip_list:iiiiiiiiiiiiiiiiiiii::::',rtn_ip_list
    return rtn_ip_list
################################################################################
    


class MyClient:   
  
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
    def download(self,file_name=None):
        print '###################start down:'+file_name
        self.sock.sendall('file:%s'%(file_name)) #send file_name to server and waiting for data
        savedFileName = "../download/"+str(time.time()).replace('.','-')+"_"+file_name
        f = open(savedFileName, 'wb')   
        while True:   
            data = self.sock.recv(1024)
            if not data:
                break
            if data == 'EOF':
                #print '###################EOF:'+file_name
                break  
            f.write(data)   
               
        f.flush()   
        f.close()   
        
        #print '###################close socket:'+file_name
        #self.sock.sendall('bye')   #to notice server to close connection
        self.sock.close()
        print file_name+':download finished and Disconnected' 
        
        end_time = time.time() #timestamp when file download finished
        fileSize = os.path.getsize(savedFileName)
        time.sleep(2)
        #os.system("rm -rf %s"%(savedFileName)) ##delete file
        #print '*****************delete:'+file_name
        if os.path.exists(savedFileName):
            os.remove(savedFileName)
        #print '*****************delete end:'+file_name
            
        return (self.start_time,end_time,end_time-self.start_time,file_name,fileSize)


def downloadThread(taskid,file_name,serverip=SOCKET_SERVER_IP):
    try:
        client = MyClient(server_ip=serverip)   
        if client.connect():
            #print "filename:"+file_name
            
            tmpTuple = (start_time,end_time,intervalTime,filename,filesize) = client.download(file_name)
            
            f = open("../log/downloadinfo-%s.txt"%(file_name),"a")
            downinfo = "%s\t%s\t%s\t%s\t%s\t%s\n"%(start_time,end_time,intervalTime,filename,filesize,serverip)
            f.write(downinfo)
            f.flush()
            f.close()
            taskQueue.put(taskid)   #insert task
            #print tmpTuple
        
    except:
        taskQueue.put(taskid)   
    
        
        
    print 'finish download,task_id:'+str(taskid)

if __name__ == '__main__':
    #initial threads
    threads = []
    for i in range(0,THREAD_NUM):
        threads.append(threading.Thread(None))
#     for i in threads:
#         print i,type(i)

    #init task queue
#     for k,v in taskQueueDic.items():
#         taskQueue.put(k)

    #change to 40 times
    task_num = 1
    for i in xrange(0,task_num):
        taskQueue.put(i)
        
    #taskQueue.put(10)
    while task_num > 0:
        taskid = 9#taskQueue.get()%10 #block until task was not empty
        #print 'tasktttttttttttttttttt:',task_num,taskid
        file_name = taskQueueDic[taskid]
        file_addr_list = monitorScheduler(fileAddrDic[file_name],False) ########scheduler##########
        print 'fffffffffffffffffffffffffffffffffffff',file_addr_list  
 
        st = time.time()
        thread_list = []
        for index in xrange(0,ERASURE_CODE):    
            thread_list.append(threading.Thread(target=downloadThread,args=(taskid,file_name,file_addr_list[index])))
        
        for index in xrange(0,len(thread_list)):
            thread_list[index].start()
        for index in xrange(0,len(thread_list)):
            thread_list[index].join()  #block until all threads are done

        et = time.time()
        print 'delay:',et-st
        task_num = task_num - 1
         
    


