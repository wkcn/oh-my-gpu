import json
import requests
import config

PORT = config.PORT 
SERVER_IP = config.SERVER_IP

SERVER_ADDRESS = "http://{}:{}".format(SERVER_IP, PORT) 
print (SERVER_ADDRESS)

QUERY_ADDR = SERVER_ADDRESS + '/query'

data = {"opcode" : 0}
headers = {'Content-Type': 'application/json'}
req = requests.post(QUERY_ADDR, data = json.dumps(data).encode(), headers = headers)
js_recv = json.loads(req.json())
state, process = js_recv

print (state[0]["memory.total"])
