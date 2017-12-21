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
    req = requests.post(QUERY_ADDR, data = bjson, headers = headers, timeout = 10)
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
    return lst

def mem2value(mem):
    return int(mem.split('M')[0])

def get_gpu_score(gpu_state):
    score = 0
    for g in gpu_state:
        f = mem2value(g["memory.free"])
        if f > score:
            score = f
    return score

def get_gpu_info():
    '''
        [(server_name, [state, process]), ...]
    '''
    data = {"opcode" : "gpu_info"}
    info = send_json(data)
    for name, s in info:
        if s is not None:
            print ("Connecting %s Successfully" % name)
        else:
            print ("Connecting %s Fail" % name, e)
    return info

def update_oh_my_gpu():
    send_json({"opcode" : "update_oh_my_gpu"})

update_oh_my_gpu()

info = get_gpu_info()
info.sort(key = lambda g : get_gpu_score(g[1][0]), reverse = True)
for m in info:
    state = m[1][0]
    state.sort(key = lambda m : mem2value(m["memory.free"]), reverse = True)
    print ("%s :" % m[0])
    for g in state:
        print ("    %s %s" % (g["gpu_id"], g["memory.free"]))
    print ("=============================")
