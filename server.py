import gpu_query
import socket
import json
from flask import Flask, request, jsonify
import config

PORT = config.PORT 
HOST_IP = socket.gethostbyname(socket.gethostname())
print ("HOST IP: {}".format(HOST_IP))

app = Flask(__name__)

@app.route('/query', methods = ['POST'])
def query():
    js_recv = request.json
    opcode = js_recv["opcode"]
    if opcode == 0:
        state, process = gpu_query.get_gpu_info()
        js_sent = json.dumps([state, process])
        return jsonify(js_sent)

if __name__ == '__main__':
    app.run(host = HOST_IP, port = PORT, debug = True)
