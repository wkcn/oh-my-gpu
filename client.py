import json
import requests
import config

data = {"opcode" : 0}
bjson = json.dumps(data).encode()
headers = {'Content-Type': 'application/json'}

for addr in config.SERVER_ADDRS:
    QUERY_ADDR = 'http://%s/query' % addr
    req = requests.post(QUERY_ADDR, data = bjson, headers = headers)
    js_recv = json.loads(req.json())
    state, process = js_recv
    print (state[0]["memory.total"])
