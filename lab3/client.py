import zmq
import sys
import time
from signal import signal, alarm, SIGALRM

signal(SIGALRM, lambda x,y:(1/0))


class Client():
    def __init__(self, name):
        self.context = zmq.Context()        
        self.pubname = self.context.socket(zmq.PUSH)
        self.pubname.connect("tcp://127.0.0.1:5677")      
        
        self.sock = self.context.socket(zmq.SUB)
        self.sock.setsockopt(zmq.SUBSCRIBE,b'')
        self.sock.connect("tcp://127.0.0.1:5678")

        self.clientname = name

    def initiateClient(self,name):
        self.pubname.send_string(name)
        self.message = self.sock.recv()
        self.message =  self.message.decode('utf-8')
        #print(self.message)
        
    
    def callserver(self,name):
        while 1:
            try: 
                while True:
                    try:                       
                        alarm(10)
                        val = input("\n[" + self.clientname + "] >")
                        self.initiateClient("[" + self.clientname + "] >" + val) 
                    except ZeroDivisionError:
                        self.message = self.sock.recv()
                        self.message =  self.message.decode('utf-8')
                        try:
                            key, value = self.message.split(":")    
                        except ValueError:
                            print(self.message) 
                        else:
                            if key.strip() != "[" + self.clientname +"]":
                                print(self.message) 
                        
                        
                            #client_inst.callserver(val)  
            except KeyboardInterrupt:
                break                           
        
    
def callClient(name):
    client_inst = Client(name)
    client_inst.initiateClient(name)
    client_inst.callserver(name)
    
if __name__ == '__main__':
    cmdargs = str(sys.argv[1])
    callClient(cmdargs)
