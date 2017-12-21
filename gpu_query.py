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
    return [line.strip() for line in lines]

if __name__ == "__main__":
    print (query_gpu("query-gpu", ["uuid", "memory.free", "memory.total"]))
    print (query_gpu("query-compute-apps", ["gpu_uuid", "name", "pid", "used_memory"]))
