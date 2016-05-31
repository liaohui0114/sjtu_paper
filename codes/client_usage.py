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
    #print 'downloadThread,thread_name=',threading.current_thread().getName()
    
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
    
    
    #time.sleep(random.randint(0,10))
    #print 'finish download,task_id:'+str(taskid)
    #print 'downloadThread,thread_name=',threading.current_thread().getName()



def weibullThread(taskid,file_name,file_addr_list,download_file_name):
    print 'weibullThread,thread_name=%s,file_name=%s,taskid=%s'%(threading.current_thread().getName(),file_name,taskid)
    st = time.time()
    thread_list = []
    for index in xrange(0,ERASURE_CODE_K):    
        thread_list.append(threading.Thread(target=downloadThread,args=(taskid,file_name,file_addr_list[index])))
    
    for index in xrange(0,len(thread_list)):
        thread_list[index].start()
    for index in xrange(0,len(thread_list)):
        thread_list[index].join()  #block until all threads are done
    

    et = time.time()
    delay = et-st
    #print 'delay:',delay
    #tmp_file_name =  "../log/erasure_code_%s_%s_%s_%s.txt"%(ERASURE_CODE_N,ERASURE_CODE_K,key,file_name)
    tmp_file_name = download_file_name
    #print tmp_file_name

    #record delay and file_ips,(start_timestamp,end_timestamp,delay,ip_1,ip2,***,ip_n)
    f = open(tmp_file_name,"a")
    downinfo = "%s\t%s\t%s"%(st,et,delay)
    for i in xrange(ERASURE_CODE_K):
        downinfo = downinfo + "\t" + file_addr_list[i]
    downinfo = downinfo + "\n"
    f.write(downinfo)
    f.flush()
    f.close()
    print 'finish weibullThread,thread_name=%s,taskid=%s'%(threading.current_thread().getName(),taskid)

##weibull distribution
def weibull_main():
    
    schedulable = {'normal':False,'scheduled':True}
    #taskQueue.put(10)
    for key,val in schedulable.items():
        for counter in xrange(0,10):

            task_num = 10

            while task_num > 0:
                print '***********%s,file:%s,task_num:%s'%(key,counter,task_num)
                taskid = counter#taskQueue.get()%10 #block until task was not empty
                #print 'tasktttttttttttttttttt:',task_num,taskid
                file_name = taskQueueDic[taskid]
                #every request include WEIBULL_NUM_PER_REQUEST download task
                for i in xrange(WEIBULL_NUM_PER_REQUEST):
                    file_addr_list = monitorScheduler(fileAddrDic[file_name],val) ########scheduler##########
                    print 'WEIBULL_NUM_PER_REQUEST,i=%s,file_addr_list=%s'%(i,file_addr_list)
                    download_file_name =  "../log/erasure_code_%s_%s_%s_%s.txt"%(ERASURE_CODE_N,ERASURE_CODE_K,key,file_name)
                    download_thread = threading.Thread(target=weibullThread,args=(taskid,file_name,file_addr_list,download_file_name))
                    download_thread.start()

                    time.sleep(2) #because monitor was not that real-time
                    

                time.sleep(WEIBULL_INTER_ARRIVAL) ##inter arrival follow weibull distribution
                task_num = task_num - 1
            time.sleep(10) ##next task

##normal
def normal_main():
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
    
    # for i in xrange(0,task_num):
    #     taskQueue.put(i)
    schedulable = {'normal':False,'scheduled':True}
    #taskQueue.put(10)
    for key,val in schedulable.items():
        task_num = 1
        while task_num > 0:
            for counter in xrange(0,10):
                taskid = counter#taskQueue.get()%10 #block until task was not empty
                #print 'tasktttttttttttttttttt:',task_num,taskid
                file_name = taskQueueDic[taskid]
                file_addr_list = monitorScheduler(fileAddrDic[file_name],val) ########scheduler##########
                print 'fffffffffffffffffffffffffffffffffffff',file_addr_list  
         
                st = time.time()
                thread_list = []
                for index in xrange(0,ERASURE_CODE_K):    
                    thread_list.append(threading.Thread(target=downloadThread,args=(taskid,file_name,file_addr_list[index])))
                
                for index in xrange(0,len(thread_list)):
                    thread_list[index].start()
                for index in xrange(0,len(thread_list)):
                    thread_list[index].join()  #block until all threads are done
                
                et = time.time()
                delay = et-st
                #print 'delay:',delay
                tmp_file_name =  "../log/erasure_code_4_2_%s_%s.txt"%(key,file_name)
                #print tmp_file_name

                f = open(tmp_file_name,"a")
                downinfo = "%s\t%s\t%s\t%s\t%s\n"%(st,et,delay,file_addr_list[0],file_addr_list[1])
                f.write(downinfo)
                f.flush()
                f.close()

                time.sleep(10)

            task_num = task_num - 1
            time.sleep(10)
def usage_test_main():
        #initial threads
    threads = []
    for i in range(0,THREAD_NUM):
        threads.append(threading.Thread(None))

    #schedulable = {'normal':False,'scheduled':True}
    schedulable = {'normal':False,}
    #taskQueue.put(10)
    for key,val in schedulable.items():
        task_num = 20
        while task_num > 0:
            for counter in xrange(2,6):
                taskid = counter#taskQueue.get()%10 #block until task was not empty
                #print 'tasktttttttttttttttttt:',task_num,taskid
                file_name = taskQueueDic[taskid]
                file_addr_list = monitorScheduler(fileAddrDic[file_name],val) ########scheduler##########
                print 'fffffffffffffffffffffffffffffffffffff',file_addr_list  
         
                st = time.time()
                thread_list = []
                for index in xrange(0,ERASURE_CODE_K):    
                    thread_list.append(threading.Thread(target=downloadThread,args=(taskid,file_name,file_addr_list[index])))
                
                for index in xrange(0,len(thread_list)):
                    thread_list[index].start()
                for index in xrange(0,len(thread_list)):
                    thread_list[index].join()  #block until all threads are done
                
                et = time.time()
                delay = et-st
                #print 'delay:',delay
                tmp_file_name =  "../log/erasure_code_%s_%s_%s_%s.txt"%(ERASURE_CODE_N,ERASURE_CODE_K,key,file_name)
                #print tmp_file_name

                f = open(tmp_file_name,"a")
                downinfo = "%s\t%s\t%s\t%s\t%s\n"%(st,et,delay,file_addr_list[0],file_addr_list[1])
                f.write(downinfo)
                f.flush()
                f.close()


            task_num = task_num - 1
            

if __name__ == '__main__':
    #normal_main()
    weibull_main()

         
    


