from flask import Flask, request, jsonify
import client

HOST_IP = "0.0.0.0"
PORT = 666

app = Flask(__name__)

@app.route('/')
def hello():
    info = client.get_gpu_info()
    buf = client.get_rest_mem(info)
    buf += '\n'
    buf += client.get_user_use(info)
    html = '''
        <html>
            <head>
                <title> oh-my-gpu </title>
            </head>
            <body>
                %s
            </body>
        </html>
    ''' %  buf.replace('\n', '<Br/>').replace('\t', '&#9;')
    return html

if __name__ == '__main__':
    app.run(host = HOST_IP, port = PORT, debug = False)
