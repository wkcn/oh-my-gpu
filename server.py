import gpu_query
import socket
import json
import os
from flask import Flask, request, jsonify
import config

PORT = config.PORT 
HOST_IP = "0.0.0.0" 
print ("HOST IP: {}".format(HOST_IP))

app = Flask(__name__)

@app.route('/query', methods = ['POST'])
def query():
    js_recv = request.json
    opcode = js_recv["opcode"]
    if opcode == "gpu_info":
        state, process = gpu_query.get_gpu_info()
        js_sent = json.dumps([state, process])
        return jsonify(js_sent)
    elif opcode == "update_oh_my_gpu":
        print ("Update oh-my-gpu")
        os.system("git pull")
        print ("Update Finished")
    print ("Invalid Code: {}".format(opcode))
    return ""

if __name__ == '__main__':
    app.run(host = HOST_IP, port = PORT, debug = True)
