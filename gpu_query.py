import psutil
from gpus import nv

def get_gpu_info():
    state = [] # uuid, memory.free, memory.toal
    process = [] # uuid, process_name, pid, used_memory
    for g in [nv]:
        state.extend(g.get_gpu_state())
        process.extend(g.get_gpu_process())

    uuid2gid = dict() # uuid -> gid
    for i, g in enumerate(state):
        uuid2gid[g[0]] = i

    for i, p in enumerate(process):
        uuid = p[0]
        gid = uuid2gid[uuid]
        process[i][0] = gid

    for i, p in enumerate(process):
        pro = psutil.Process(int(p[2]))
        username = pro.username()
        print (username)

if __name__ == "__main__":
    print (get_gpu_info())
