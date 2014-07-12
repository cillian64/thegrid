"""
control.py

The Grid Control System

Hooks together the hardware interface, pattern modules, people tracking, and an
HTTP API for remote control.
"""

import time
import queue
from multiprocessing import Manager, Queue

from .api import API
from .tracking import Tracking


def main():
    cmd_queue = Queue()
    tracking_manager = Manager()
    tracking_dict = tracking_manager.dict()

    tracking = Tracking(tracking_dict)
    api = API(8080, 'password', cmd_queue)

    while True:
        print("Current tracking:", tracking_dict)
        try:
            cmd = cmd_queue.get_nowait()
            print("Received command:", cmd)
            if cmd[0] == "stop":
                break
        except queue.Empty:
            pass

        time.sleep(1)

    print("Shutting down")
    tracking.stop()
    api.stop()


if __name__ == "__main__":
    main()
