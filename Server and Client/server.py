import asyncio

data = ""
class ClientServerProtocol(asyncio.Protocol):
    
    def process_data(self, data_1):
        global data
        if not data_1:
            return "error\nwrong command\n\n"
        
        data_2 = data_1.replace("\n", "").split()
        if data_2[0] == "put":
            if data.find(data_1.replace("put ", "")) == -1:
                data += data_1.replace("put ", "")
            else:
                data = data.replace(data_1.replace("put ", ""), "")
                data += data_1.replace("put ", "")
            return "ok\n\n"
            
        elif data_2[0] == "get":
             out = "ok\n"
             key = data_2[1]
             inf = data.split("\n")
             if key == "*":
                 out += data
             else:
                 for m in inf:
                     try:
                         if m.split()[0] == key:
                             out += m
                             out += "\n"
                     except:
                        pass
             out += "\n"
             return out
        else:
            return "error\nwrong command\n\n"
        
    def connection_made(self, transport):
         self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())
        
loop = asyncio.get_event_loop()
coro = loop.create_server(ClientServerProtocol, "127.0.0.1", 8888)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()


