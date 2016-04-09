#!/usr/bin/python 
#coding:utf-8 
import sys,os
import socket, time
import threading
import random
import Queue
#liaohui

SOCKET_SERVER_IP = '127.0.0.1'
SOCKET_SERVER_PORT = 50000
SOCKET_BUFFER_SIZE = 1024  #packet size of socket(send/receive) 
SOCKET_TIME_OUT = 8
THREAD_NUM = 5
taskQueueDic = {1:"1.png",
           2:"2.png",
           3:"3.png",
           4:"4.png",
           5:"5.png",
           6:"6.png",
           7:"7.png",
           8:"8.png",
           9:"9.mkv",
           10:"10.mkv",}

fileAddrDic = {"1.png":["127.0.0.1"],
           "2.png":["127.0.0.1"],
           "3.png":["127.0.0.1"],
           "4.png":["127.0.0.1"],
           "5.png":["127.0.0.1"],
           "6.png":["127.0.0.1"],
           "7.png":["127.0.0.1"],
           "8.png":["127.0.0.1"],
           "9.mkv":["127.0.0.1"],
           "10.mkv":["127.0.0.1"],}

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

taskCounter = 1



class MyClient:   
  
    def __init__(self,server_ip=SOCKET_SERVER_IP,server_port=SOCKET_SERVER_PORT):   
        print 'Prepare for connecting...'
        self.server_ip = server_ip
        self.server_port = server_port
  
    def connect(self):
        self.start_time = time.time() # timestamp when download start
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.sock.connect((self.server_ip,self.server_port))   
        print 'connected'
        return True
    def download(self,file_name=None):
        self.sock.sendall('file:%s'%(file_name)) #send file_name to server and waiting for data
        savedFileName = str(time.time()).replace('.','-')+"_"+file_name
        f = open(savedFileName, 'wb')   
        while True:   
            data = self.sock.recv(1024)
            if data == 'EOF':
                break  
            f.write(data)   
               
        f.flush()   
        f.close()   
        
        
        #self.sock.sendall('bye')   #to notice server to close connection
        self.sock.close()
        print file_name+':download finished and Disconnected' 
        
        end_time = time.time() #timestamp when file download finished
        fileSize = os.path.getsize(savedFileName)
        time.sleep(2)
        #os.system("rm -rf %s"%(savedFileName)) ##delete file
        if os.path.exists(savedFileName):
            os.remove(savedFileName)
            
        return (self.start_time,end_time,end_time-self.start_time,savedFileName,fileSize)


def downloadThread(taskid,file_name,server_ip=SOCKET_SERVER_IP):
    client = MyClient(server_ip=SOCKET_SERVER_IP)   
    if client.connect():
        taskingQueueDic[taskid] = True #to start task
        tmpTuple = (start_time,end_time,intervalTime,filename,filesize) = client.download(file_name)
        taskingQueueDic[taskid] = False  #this task is finished
        f = open("log/downloadinfo.txt","a")
        downinfo = "%s\t%s\t%s\t%s\t%s\n"%(start_time,end_time,intervalTime,filename,filesize)
        f.write(downinfo)
        f.flush()
        f.close()
        #print tmpTuple
        
        
        
    print 'finish download,task_id:'+str(taskid)

if __name__ == '__main__':
    #initial threads
    threads = []
    for i in range(1,THREAD_NUM+1):
        threads.append(threading.Thread(None))
#     for i in threads:
#         print i,type(i)
    while True:
        if not taskingQueueDic[taskCounter]:
            
            #to find a thread which is idle
            for num,item in enumerate(threads):
                if not item.is_alive():
                #to avoid multi threads doing one task
                
                    print 'task_id:'+str(taskCounter)
                    
                    file_name = taskQueueDic[taskCounter]
                    addrPos = random.randint(0,len(fileAddrDic[file_name])-1) #rand select addr of the file
                    file_addr = fileAddrDic[file_name][addrPos]
                    
                    print file_name,file_addr
                    
                    item = threading.Thread(target=downloadThread,args=(taskCounter,file_name,file_addr))
                    item.start()
                    break
                    
        taskCounter = (taskCounter)%len(taskQueueDic)+1 #to get next task in queue
        time.sleep(1)        

         
    