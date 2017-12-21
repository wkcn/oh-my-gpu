import json
import requests
import config

def send_json(data):
    bjson = json.dumps(data).encode()
    headers = {'Content-Type': 'application/json'}

    lst = []
    for addr in config.SERVER_ADDRS:
        QUERY_ADDR = 'http://%s/query' % addr
        req = requests.post(QUERY_ADDR, data = bjson, headers = headers)
        js_recv = json.loads(req.json())
        lst.append(js_recv)
    return lst

def get_gpu_info():
    data = {"opcode" : "gpu_info"}
    lst = send_json(data)
    for d in lst:
        print (d)

def update_oh_my_gpu():
    send_json({"opcode" : "update_h_my_gpu"})

get_gpu_info()
