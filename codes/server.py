#!/usr/bin/python 
#coding:utf-8 
import SocketServer, time,sys
  
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
            elif receivedData == 'bye':   
                break  
  
        self.request.close()   
           
        print 'Disconnected from', self.client_address   
  
if __name__ == '__main__':   
    print 'Server is started\nwaiting for connection...\n'
    serverip = sys.argv[1]
    srv = SocketServer.ThreadingTCPServer((serverip, 50000), MyServer)   
    srv.serve_forever()  