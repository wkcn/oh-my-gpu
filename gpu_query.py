import psutil
from gpus import nv
from utils import ps

def get_gpu_info():
    state = [] # uuid, memory.free, memory.toal
    process = [] # uuid, process_name, pid, used_memory | username, name
    for g in [nv]:
        state.extend(g.get_gpu_state())
        process.extend(g.get_gpu_process())
    uuid2gid = dict() # uuid -> gid
    
    for i, g in enumerate(state):
        uuid2gid[g["uuid"]] = i
        g["gpu_id"] = i
        
    for i, p in enumerate(process):
        uuid = p["uuid"]
        gid = uuid2gid[uuid]
        process[i]["gpu_id"] = gid
        
    ps.update_info()
    for i, p in enumerate(process):
        pid = p["pid"]
        username, pname = ps.get_username_from_pid(pid) 
        p["username"] = username
        p["name"] = pname
    return state, process

if __name__ == "__main__":
    print (get_gpu_info())
