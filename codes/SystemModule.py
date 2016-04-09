#!/usr/bin/env python
# -*- coding:utf-8 -*-
import psutil
import time
import collections

class SysInfo(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def GetCPUPercent(self,cpuinterval=1):
        return psutil.cpu_percent(interval=1)
    
    def GetMemory(self):
        return psutil.virtual_memory()
    
    def GetDiskUsage(self,path="/"):
        return psutil.disk_usage(path)
    
    def GetDiskIO(self):
        return psutil.disk_io_counters()
    
    def GetDiskIOInterval(self,interval=5):
        diskinfo = psutil.disk_io_counters()
        time.sleep(interval)
        diskinfo2 = psutil.disk_io_counters()
        
        rc = diskinfo2[0]-diskinfo[0]
        wc = diskinfo2[1]-diskinfo[1]
        rb = diskinfo2[2]-diskinfo[2]
        wb = diskinfo2[3]-diskinfo[3]
        
        sdisk = collections.namedtuple('intervaldiskio','read_count write_count read_bytes write_bytes')
        
        return sdisk(read_count=rc, write_count=wc, read_bytes=rb, write_bytes=wb)
    
    def GetNetworkIO(self):
        return psutil.net_io_counters()
    
    def GetNetworkIOInterval(self,interval=1):
        netio =  psutil.net_io_counters()
        time.sleep(interval)
        netio2 = psutil.net_io_counters()
        bs = netio2[0] - netio[0]
        br = netio2[1] - netio[1]
        ps = netio2[2] - netio[2]
        pr = netio2[3] - netio[3] 
        snet = collections.namedtuple('intervalnetio','bytes_sent bytes_recv packets_sent packets_recv')
        return snet(bs,br,ps,pr)
    
    def GetCurrentTime(self):
        curtimestamp = time.time()
        curtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(curtimestamp))
        snet = collections.namedtuple('currenttime','current_timestamp current_time')
        return snet(curtimestamp,curtime)

        
    
    
