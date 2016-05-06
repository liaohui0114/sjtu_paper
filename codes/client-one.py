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
#target=0:by net_send;1:by_recv;2:by delay
def getMinIP(monitor_dict,target=0):
    tmp = sys.maxint
    tmp_ip = ''
    for key,val in monitor_dict.items():
        if float(val[0])<tmp:
            tmp = float(val[0])
            tmp_ip = key 
    return tmp_ip

def monitorScheduler(ip_list,isScheduled = False):
    if not isScheduled:
        return ip_list[random.randint(0,len(ip_list)-1)] #return random ip from ip_list

    #scheduling
    monitor_dict = {}
    for ipaddr in ip_list:
        f = open("../log/monitorinfo-%s.txt"%(ipaddr),"r") #########################
        last_line = f.readlines()[-1]
        f.close()

        monitor_info = last_line.split()
        monitor_dict[ipaddr] = monitor_info
    #print monitor_dict
    tmp_ip = getMinIP(monitor_dict,0)
    #print 'bbbb',tmp_ip
    return tmp_ip
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
    task_num = TASK_NUMBER
    for i in xrange(0,task_num):
        taskQueue.put(i)
        
    #taskQueue.put(10)
    while task_num > 0:
        
        #if not taskQueue.empty():

        hasIdle = False
        
        #to find a thread which is idle
        for index in range(0,len(threads)):
            if not threads[index].is_alive():
            #to avoid multi threads doing one task
                taskid = taskQueue.get()%10 #block until task was not empty
                #print 'tasktttttttttttttttttt:',task_num,taskid
                file_name = taskQueueDic[taskid]
                #addrPos = random.randint(0,len(fileAddrDic[file_name])-1) #rand select addr of the file
                #addrPos = random.randint(0,0)
                #file_addr = fileAddrDic[file_name][addrPos]
                file_addr = monitorScheduler(fileAddrDic[file_name],False) ########scheduler##########
                #print 'fffffffffffffffffffffffffffffffffffff',file_addr
                threads[index] = threading.Thread(target=downloadThread,args=(taskid,file_name,file_addr))
                threads[index].start()

                hasIdle = True
                break
        if hasIdle == True:
            time.sleep(0.5)            
            task_num = task_num - 1
        else:
            time.sleep(1)    

         
    


