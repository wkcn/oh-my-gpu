import socket
import json
import requests

PORT = 690
HOST_IP = socket.gethostbyname(socket.gethostname())
print ("HOST IP: {}".format(HOST_IP))

# for test
SERVER_IP = HOST_IP

SERVER_ADDRESS = "http://{}:{}".format(SERVER_IP, PORT) 
print (SERVER_ADDRESS)

data = {"opcode" : 0}
req = requests.post(SERVER_ADDRESS + "/query", json = data)
js_recv = json.loads(req.json())
state, process = js_recv

print (state[0]["memory.total"])
