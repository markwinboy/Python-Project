import time
import socket


class ClientError(Exception):
    pass

class Client:
    def __init__(self,host,port,timeout=None):
        self.host = host
        self.port = int(port)
        if timeout == None:
            timeout = int(time.time())
        elif timeout == "":
            timesout = int(time.time())
        self.timeout = timeout       
        try:
            self.sock = socket.create_connection((self.host, self.port),self.timeout)  
        except:
            raise ClientError()

    def put(self,key,value,timestamp=None):
        if timestamp == None:
            timestamp = int(time.time())
        elif timestamp == "":
            timestamp = int(time.time())
        try:
            self.sock.sendall(("put "+str(key)+" "+str(value)+" "+str(timestamp)+"\n").encode())
            w = self.sock.recv(1024).decode()
        except:
            raise ClientError()
        if w=="ok\n\n":
            pass

    def get(self,key):
        d=dict()
        try:
            self.sock.sendall(("get "+str(key)+"\n").encode())
            q = self.sock.recv(1024).decode()
        except:
            raise ClientError()
        if  q == "ok\n\n":
            pass
        elif q=="error\nwrong command\n\n":
            raise ClientError()
        
        q=q.split("\n")
        for i in q:
            if len(i.split()) == 3:
                i=i.split()
                if i[0] in d:
                    d[i[0]].append((int(i[2]),float(i[1])))
                else:
                    d[i[0]]=[(int(i[2]),float(i[1]))]
        return d
        



    
