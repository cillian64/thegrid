"""
api.py

HTTP interface for Android and web apps.
"""

import logging
from multiprocessing import Process
from flask import Flask, Response, request

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Welcome to The·Grid"


@app.route('/command', methods=['POST'])
def command():
    auth = request.authorization
    if not auth or not auth.password == app.config['PASSWORD']:
        logger.warning("Unauthorized API request from {}".format(
            request.headers['REMOTE_ADDR']))
        return Response('Unauthorized', 401)

    command = request.form['cmd']
    value = request.form['val']
    logger.info("Enqueueing API command ({}, {})".format(command, value))
    app.config['QUEUE'].put((command, value))
    return "OK"


def run_server(port, password, queue):
    app.config['PASSWORD'] = password
    app.config['QUEUE'] = queue
    logger.info("API server starting up")
    app.run(host='0.0.0.0', port=port)


class API:
    def __init__(self, port, password, queue):
        self.server = Process(
            target=run_server, args=(port, password, queue), daemon=True)
        self.server.start()

    def stop(self):
        self.server.terminate()
        self.server.join()

    def __del__(self):
        self.stop()
