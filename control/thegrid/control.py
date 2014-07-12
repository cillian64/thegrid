"""
control.py

The Grid Control System

Hooks together the hardware interface, pattern modules, people tracking, and an
HTTP API for remote control.
"""

import time
import queue
import logging
from multiprocessing import Manager, Queue

from .api import API
from .tracking import Tracking
from . import patterns
from . import sinks


logger = logging.getLogger("thegrid.control")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")

    logger.info("The·Grid Control starting up...")

    cmd_queue = Queue()
    tracking_manager = Manager()
    tracking_dict = tracking_manager.dict()

    tracking = Tracking(tracking_dict)
    api = API(8080, 'password', cmd_queue)

    while True:
        logger.info("Current tracking: {}".format(tracking_dict))
        try:
            cmd = cmd_queue.get_nowait()
            print("Received command:", cmd)
            if cmd[0] == "stop":
                break
        except queue.Empty:
            pass

        time.sleep(1)

    logger.info("Control shutting down")
    tracking.stop()
    api.stop()


if __name__ == "__main__":
    main()
