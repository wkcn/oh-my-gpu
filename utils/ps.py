import os
import platform
import psutil

platform_system = platform.system()
assert platform_system in ["Linux", "Windows"], "Only Support for Windows and Linux"
LINUX = (platform_system == "Linux")

def get_loc_value(loc_str, pattern, context):
    '''
    Name
    value
    '''
    loc_i = pattern.find(loc_str)
    left = loc_i
    right = loc_i
    while left > 0 and context[left - 1] != ' ':
        left -= 1
    while right + 1 < len(context) and context[right + 1] != ' ':
        right += 1
    return context[left:right + 1].strip()  

def get_loc_value2(loc_str, context):
    '''
    Name
    ========
    value
    '''
    loc_i = context[0].find(loc_str)
    left = loc_i
    right = loc_i
    ep = context[1]
    while left > 0 and ep[left - 1] == '=':
        left -= 1
    while right + 1 < len(ep) and ep[right + 1] == '=':
        right += 1
    return context[2][left:right + 1].strip()
    
def get_column2(loc_str, context):
    '''
    Name
    ========
    value
    '''
    loc_i = context[0].find(loc_str)
    
    ep = context[1]
    left = loc_i
    right = loc_i
    
    while left > 0 and ep[left - 1] == '=':
        left -= 1
    while right + 1 < len(ep) and ep[right + 1] == '=':
        right += 1
    return [context[i][left:right + 1].strip() for i in range(2, len(context))]




def get_task_list():
    cmd = 'tasklist'
    lines = os.popen(cmd).readlines()
    
    pnames = get_column2("Image Name", lines[1:])
    pids = get_column2("PID", lines[1:])
    sids = get_column2("Session#", lines[1:])
    res = dict()
    for pid, pname, sid in zip(pids, pnames, sids):
        res[int(pid)] = dict(pname = pname, sid = int(sid) )
    return res


def get_session_list():
    cmd = 'query session'
    lines = os.popen(cmd).readlines()
    pattern = lines[0]
    res = dict()
    for i in range(1, len(lines)):
        s = lines[i]
        sid = get_loc_value("ID", pattern, s)
        uname = get_loc_value("USERNAME", pattern, s)
        res[int(sid)] = uname
    return res
        
TASK_LIST = dict() # PID -> INFO   
SESSION_LIST = dict() # SID -> NAME    
def update_info():
    if LINUX:
        return
    # For windows
    global TASK_LIST
    global SESSION_LIST
    TASK_LIST = get_task_list()
    SESSION_LIST = get_session_list()

def get_username_from_pid(pid):
    if LINUX:
        p = psutil.Process(pid)
        return p.username(), p.cwd() + "|" + p.name()
    pinfo = TASK_LIST[pid]        
    pname = pinfo["pname"]
    sid = pinfo["sid"]
    username = SESSION_LIST[sid]
    return username, pname

if __name__ == "__main__":
    pid = os.getpid()
    print (get_username_from_pid(pid))
