import json
import requests
import config
import threading
try:
    import Queue
except:
    import queue as Queue

TIMEOUT = 10

for i, a in enumerate(config.SERVER_ADDRS):
    if type(a) == str:
        config.SERVER_ADDRS[i] = [a, a]

def thread_get_gpu_info(name, addr, q, bjson):
    headers = {'Content-Type': 'application/json'}
    QUERY_ADDR = 'http://%s/query' % addr
    req = requests.post(QUERY_ADDR, data = bjson, headers = headers, timeout = TIMEOUT)
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
    for a in config.SERVER_ADDRS:
        name, addr = a
        ts.append(threading.Thread(target = thread_get_gpu_info, args = (name, addr, q, bjson)))
    for t in ts:
        t.setDaemon(True)
        t.start()
    for t in ts:
        t.join()
    # Get Information
    lst = []
    vis = set()
    while not q.empty():
        r = q.get()
        lst.append(r)
        vis.add(r[0])
    for a in config.SERVER_ADDRS:
        name = a[0]
        if name not in vis:
            lst.append((name, None))
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
    buf = ''
    data = {"opcode" : "gpu_info"}
    info = send_json(data)
    valid = []
    for name, s in info:
        if s is not None:
            buf += ("Connecting %s Successfully" % name) + '\n'
            valid.append((name, s))
        else:
            buf += ("Connecting %s Fail" % name) + '\n'
    buf += '\n'
    return buf, valid

def update_oh_my_gpu():
    send_json({"opcode" : "update_oh_my_gpu"})


def get_rest_mem(info):
    buf = ''
    info.sort(key = lambda g : get_gpu_score(g[1][0]), reverse = True)
    for i, m in enumerate(info):
        state = m[1][0]
        state.sort(key = lambda m : mem2value(m["memory.free"]), reverse = True)
        buf += "%s [%d]:" % (m[0], i)
        buf += '\n'
        for g in state:
            buf += ("    %s %s" % (g["gpu_id"], g["memory.free"]))
            buf += '\n'
        buf += ("=============================")
        buf += '\n'
    return buf

def show_rest_mem(info):
    print (get_rest_mem(info))

def get_user_use(info):
    buf = ''

    users = dict()
    for i, m in enumerate(info):
        process = m[1][1]
        for p in process:
            uuid = p["uuid"]
            used_mem = mem2value(p["used_memory"])
            username = p["username"]
            if used_mem < 200:
                continue
            if username not in users:
                users[username] = {
                        "used_mem": 0,
                        "used_gpus": set(),
                        "mem_lst": []
                }
            u = users[username]
            u["used_mem"] += used_mem
            u["used_gpus"].add(uuid)
            u["mem_lst"].append("%d:%d" % (i, used_mem))
    lst = list(users.items()) # username, infos
    for u in lst:
        u[1]["avg_mem"] = u[1]["used_mem"] // len(u[1]["used_gpus"])
    lst.sort(key = lambda u : len(u[1]["used_gpus"]), reverse = True)
    buf += ("Username\tUsed GPUs\tAVG Memory\tUsed Memory\tMemory List")
    buf += '\n'
    for u in lst:
        f = u[1]
        buf += ("%s    \t%d          \t%d          \t%d        \t%s" % (u[0], len(f["used_gpus"]), f["avg_mem"], f["used_mem"], str(f["mem_lst"])))
        buf += '\n'
    return buf

def show_user_use(info):
    print (get_user_use(info))

if __name__ == "__main__":
    update_oh_my_gpu()

    buf, info = get_gpu_info()
    print (buf)
    show_rest_mem(info)
    show_user_use(info)
