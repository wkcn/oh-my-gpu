import os

NVIDIA_SMI = "nvidia-smi"

def query_gpu(query_name, args):
    '''
    query_name:
        query_gpu
        query_compute_apps
    '''
    cmd = "%s --%s=%s --format=csv,noheader" % (NVIDIA_SMI, query_name, ','.join(args))
    lines = os.popen(cmd).readlines()
    lst = [line.strip().split(", ") for line in lines]
    pairs = [zip(args, x) for x in lst]
    return [dict(p) for p in pairs] 

def get_gpu_state():
    return query_gpu("query-gpu", ["uuid", "memory.free", "memory.total"])

def replace_key(data, oldkey, newkey):
    for i, d in enumerate(data):
        data[i][newkey] = data[i].pop(oldkey)

def get_gpu_process():
    data = query_gpu("query-compute-apps", ["gpu_uuid", "name", "pid", "used_memory"])
    replace_key(data, "gpu_uuid", "uuid")
    for d in data:
        d["pid"] = int(d["pid"])
    return data

if __name__ == "__main__":
    print (get_gpu_state())
    print (get_gpu_process())
