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
    return [line.strip().split(", ") for line in lines]

def get_gpu_state():
    return query_gpu("query-gpu", ["uuid", "memory.free", "memory.total"])

def get_gpu_process():
    return query_gpu("query-compute-apps", ["gpu_uuid", "name", "pid", "used_memory"])

if __name__ == "__main__":
    print (get_gpu_state())
    print (get_gpu_process())
