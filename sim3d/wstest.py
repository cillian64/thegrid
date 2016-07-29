import numpy as np
import json
import asyncio
import websockets


@asyncio.coroutine
def hello(websocket, path):
    i = 0
    while True:
        poles = np.zeros((7, 7, 6))
        poles[i, :] = [0, 1, 0, 3, 200, 5]
        i = (i + 1) % 7
        #i = np.random.randint(7)
        #j = np.random.randint(7)
        #poles[i, j] = [0, 1, 0, 1, 440, .6]
        #i = np.random.randint(7)
        #j = np.random.randint(7)
        #poles[i, j] = [0, 0, 1, 2, 2000, .5]
        #i = np.random.randint(7)
        #j = np.random.randint(7)
        #poles[i, j] = [1, 0, 0, 2, 3000, .6]
        yield from websocket.send(json.dumps(poles.tolist()))
        yield from asyncio.sleep(0.1)

start_server = websockets.serve(hello, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
