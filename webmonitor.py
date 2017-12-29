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

    sp = buf.split('\n')
    
    # Memory > 6G, font green
    buf = ''
    for s in sp:
        if 'MiB' in s:
            s = ' '.join(s.split()) # merge blank space
            mb = int(s.split(' ')[1])
            if mb > 6000:
                buf += '<font color="#00FF00">'
                buf += s
                buf += '</font>'
            else:
                buf += s
        else:
            buf += s
        buf += '\n'
    
    
    table =  client.get_user_use(info)
    buf += '<table border="1">'
    for line in table.split('\n'):
        buf += '<tr>'
        for e in line.split('\t'):
            buf += '<td>%s</td>' % e
        buf += '</tr>'
    buf += '</table>'
    
    html = '''
        <html>
            <head>
                <title> oh-my-gpu </title>
            </head>
            <body>
                %s
            </body>
        </html>
    ''' %  buf.replace('\n', '<Br/>')#.replace('\t', '&#9;')
    return html

if __name__ == '__main__':
    app.run(host = HOST_IP, port = PORT, debug = False)
