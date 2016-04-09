#!/usr/bin/python 
#coding:utf-8 
import sys,os
import socket, time
import threading
import random
import Queue
from variable import *


taskQueue = Queue.Queue(0)
taskCounter = 1



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
        savedFileName = str(time.time()).replace('.','-')+"_"+file_name
        f = open("../download/%s"%(savedFileName), 'wb')   
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
            taskingQueueDic[taskid] = True #to start task
            tmpTuple = (start_time,end_time,intervalTime,filename,filesize) = client.download(file_name)
            taskingQueueDic[taskid] = False  #this task is finished
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
    for i in range(1,THREAD_NUM+1):
        threads.append(threading.Thread(None))
#     for i in threads:
#         print i,type(i)
    #init task queue
    for k,v in taskQueueDic.items():
        taskQueue.put(k)
        
    #taskQueue.put(10)
    while True:
        
        #if not taskQueue.empty():
        taskid = taskQueue.get() #block until task was not empty
        
        #to find a thread which is idle
        for num,item in enumerate(threads):
            if not item.is_alive():
            #to avoid multi threads doing one task
            
                print 'task_id:'+str(taskid)
                file_name = taskQueueDic[taskid]
                addrPos = random.randint(0,len(fileAddrDic[file_name])-1) #rand select addr of the file
                file_addr = fileAddrDic[file_name][addrPos]
                item = threading.Thread(target=downloadThread,args=(taskid,file_name,file_addr))
                item.start()
                break
                    
        
        #time.sleep(1)        

         
    
