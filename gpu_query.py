from gpus import nv

def get_gpu_info():
    state = []
    process = []
    for g in [nv]:
        state.extend(g.get_gpu_state())
        process.extend(g.get_gpu_process())
    return [state, process]

if __name__ == "__main__":
    print (get_gpu_info())
