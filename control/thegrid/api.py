"""
api.py

HTTP interface for Android and web apps.
"""

from multiprocessing import Process, Queue
from functools import wraps

from flask import Flask, Response, request, g

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to The·Grid"

@app.route('/command', methods=['POST'])
def command():
    auth = request.authorization
    if not auth or not auth.password == app.config['PASSWORD']:
        return Response('Unauthorized', 401)

    command = request.DATA['cmd']
    value = request.DATA['val']
    app.config['QUEUE'].put((command, value))
    return "OK"

def run_server(port, password, queue):
    app.config['PASSWORD'] = password
    app.config['QUEUE'] = queue
    app.run(host='0.0.0.0', port=port)

class API:
    def __init__(self, port, password, queue):
        self.server = Process(target=run_server, args=(port, password, queue))
        self.server.start()

    def stop(self):
        self.server.terminate()
        self.server.join()

    def __del__(self):
        self.stop()
