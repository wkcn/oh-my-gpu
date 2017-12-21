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
    while right + 1 < len(ep) and context[right + 1] != ' ':
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


def get_username_from_pid(pid):
    try:
        if LINUX:
            return psutil.Process(pid).username()
        cmd = 'tasklist /FI "PID eq %d"' % pid
        lines = os.popen(cmd).readlines()
                
        pname = get_loc_value2("Image Name", lines[1:])
        sid = int(get_loc_value2("Session#", lines[1:]))
                        
        cmd = 'query session %d' % sid
        lines = os.popen(cmd).readlines()
        username = get_loc_value("USERNAME", lines[0], lines[1])
        return username, pname
    except:
        return "", ""

if __name__ == "__main__":
    pid = os.getpid()
    print (get_username_from_pid(pid))
