import os
import platform
import psutil

platform_system = platform.system()
assert platform_system in ["Linux", "Windows"], "Only Support for Windows and Linux"
LINUX = (platform_system == "Linux")

def get_loc_value(loc_str, pattern, context):
    loc_i = pattern.find(loc_str)
    return context[loc_i:loc_i + len(loc_str)].strip()

def get_username_from_pid(pid):
    try:
        if LINUX:
            return psutil.Process(pid).username()
        cmd = 'tasklist /FI "PID eq %d"' % pid
        lines = os.popen(cmd).readlines()
                
        sid = int(get_loc_value("Session#", lines[1], lines[3]))
                        
        cmd = 'query session %d' % sid
        lines = os.popen(cmd).readlines()
        username = get_loc_value("USERNAME", lines[0], lines[1])
        return username
    except:
        pass
if __name__ == "__main__":
    pid = os.getpid()
    print (get_username_from_pid(pid))
