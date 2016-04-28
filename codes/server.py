#!/usr/bin/python 
#coding:utf-8 
import SocketServer
import time,sys,json
import SystemModule
from variable import *

def getMonitor():
    sysinfo = SystemModule.SysInfo()
    netinfo = sysinfo.GetNetworkIOInterval(1) ##sleep 1s
    netbytesend = netinfo[0]
    netbyterecv = netinfo[1]
    return (netbytesend,netbyterecv)


class MyServer(SocketServer.BaseRequestHandler):
  
    def handle(self):   
        print 'Connected from', self.client_address   
           
        while True:   
            receivedData = self.request.recv(8192) #to get filename
            if not receivedData:   
                continue  
            elif receivedData.startswith('file'):   
                file_name = receivedData.split(':')[-1]   
                print file_name
                sfile = open("../files/%s"%(file_name), 'rb')   
                while True:   
                    data = sfile.read(1024)   
                    if not data:   
                        break  
                    while len(data) > 0:   
                        intSent = self.request.send(data)   
                        data = data[intSent:]   
                
                time.sleep(1)   #to send EOF,or will wrong
                print 'end send:'+file_name
                self.request.sendall('EOF')
                
                #self.request.close() 
                break
            elif receivedData.startswith('monitor'):
                (net_send,net_recv) = getMonitor()
                monitor_info = {KEY_NET_SEND:net_send,KEY_NET_RECV:net_recv}
                #print 'monitor_info:',monitor_info
                self.request.sendall(json.dumps(monitor_info))
                # send monitor info to agent
                break;
            elif receivedData == 'bye':   
                break  
  
        self.request.close()   
           
        print 'Disconnected from', self.client_address   
  
if __name__ == '__main__':   
    print 'Server is started\nwaiting for connection...\n'
    serverip = sys.argv[1]
    srv = SocketServer.ThreadingTCPServer((serverip, 50000), MyServer)   
    srv.serve_forever()  