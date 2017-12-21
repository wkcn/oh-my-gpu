import json
import requests
import config
import threading
try:
    import Queue
except:
    import queue as Queue

def thread_get_gpu_info(name, addr, q, bjson):
    headers = {'Content-Type': 'application/json'}
    QUERY_ADDR = 'http://%s/query' % addr
    req = requests.post(QUERY_ADDR, data = bjson, headers = headers)
    try:
        jdata = req.json()
        js_recv = json.loads(jdata)
        q.put((name, js_recv))
    except Exception as e:
        q.put((name, None))

def send_json(data):

    bjson = json.dumps(data).encode()

    ts = []
    q = Queue.Queue()
    for addr in config.SERVER_ADDRS:
        if type(addr) is str:
            addr = (addr, addr)
        name, addr = addr
        ts.append(threading.Thread(target = thread_get_gpu_info, args = (name, addr, q, bjson)))
    for t in ts:
        t.setDaemon(True)
        t.start()
    for t in ts:
        t.join()
    lst = []
    while not q.empty():
        lst.append(q.get())
    return dict(lst)

def get_gpu_info():
    data = {"opcode" : "gpu_info"}
    info = send_json(data)
    for name, s in info.items():
        if s is not None:
            print ("Connecting %s Successfully" % name)
        else:
            print ("Connecting %s Fail" % name, e)

def update_oh_my_gpu():
    send_json({"opcode" : "update_oh_my_gpu"})

get_gpu_info()
update_oh_my_gpu()
