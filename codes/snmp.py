#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import psutil #获取系统信息的python包
import SystemModule
# def getCPUsnmp(ip):
#     cpuoid = ".1.3.6.1.4.1.2021.11.11.0"
#     cmd = "snmpwalk -v 2c -c public %s %s"%(ip,cpuoid)
#     fp = os.popen(cmd) #popen返回一个文件描述符指向显示的内容
#     ftxt = fp.readlines()
#     #sleep(5)
#     ftxt = ftxt[0].split()
#     print ftxt[-1]
#     print ftxt
#     
#     
# def getCPU(interval=5):
#     #get the cpu state
#     fcpu = open('/proc/stat')
#     try:
#         lines = fcpu.readlines()
#         line= lines[0].split()
#     finally:
#         fcpu.close()
#     total1 =0.0
#     idle1 = 0.0
#     for slide in line[1:7]:
#         total1 = total1 + (float)(slide)
#         if(slide == line[4]):
#             idle1 = idle1 + (float)(slide)
# 
#     #time.sleep(5)
#     time.sleep(interval)
#     fcpu = open('/proc/stat')
#     try:
#         lines = fcpu.readlines()
#         line= lines[0].split()
#     finally:
#         fcpu.close()
#     total2 =0.0
#     idle2 = 0.0
#     for slide in line[1:7]:
#         total2 = total2 + (float)(slide)
#         if(slide == line[4]):
#             idle2 = idle2 + (float)(slide)
#     total = total2 - total1
#     idle = idle2 - idle1
#     cpu_per = 100*(total - idle)/total
#     print "cpu percentage: %0.2f %%"%cpu_per
#     return cpu_per
# 
# def getMEM():
#     #get the memory state
#     fmem = open('/proc/meminfo')
#     try:
#         lines = fmem.readlines()
#         line1 = lines[0].split()
#         line2 = lines[1].split()
#     finally:
#         fmem.close()
#     total = (float)(line1[1])
#     idle = (float)(line2[1])
#     mem_per = 100*(1-idle/total)
#     print "mem percetage: %0.2f %%"%mem_per
#     return mem_per
# 
# def getMemory(ip):
#     pass
# 
# def getBandwidth(ip):
#     pass


if __name__=="__main__":
    #print getCPU(1)

    

    #f.writelines(["liaohui","xuehua"])
    while True:
        f = open("../log/systeminfo.txt","a")
        sysinfo = SystemModule.SysInfo()
        (curtimestamp,curtime) = sysinfo.GetCurrentTime()
        cpupercent =  sysinfo.GetCPUPercent(1)  #sleep 1s
        meminfo =  sysinfo.GetMemory()
        mempercent = meminfo[2]
        diskinfo =  sysinfo.GetDiskUsage()
        diskpercent = diskinfo[3]
        
        diskioinfo =  sysinfo.GetDiskIOInterval(1) ##sleep 1s
        
        diskread = diskioinfo[0]
        diskwrite = diskioinfo[1]
        diskreadbyte = diskioinfo[2]
        diskwritebyte = diskioinfo[3]
        
        netinfo = sysinfo.GetNetworkIOInterval(1) ##sleep 1s
        netbytesend = netinfo[0]
        netbyterecv = netinfo[1]
        
        #print sysinfo.GetDiskIOInterval(5)
        #print sysinfo.GetNetworkIO()
        #print sysinfo.GetNetworkIOInterval(5)
        #sysinfolist = [curtimestamp,curtime,cpupercent,mempercent,diskpercent,diskread,diskwrite]
        sysStr = "%s\t\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n"%\
        (curtimestamp,cpupercent,mempercent,diskpercent,diskread,diskwrite,diskreadbyte,diskwritebyte,netbytesend,netbyterecv)
        
        #f.writelines(sysinfolist)
        f.write(sysStr)
        f.flush()
        f.close()
        
    print 'close'
    
    
    #print psutil.net_if_stats()
    
    
