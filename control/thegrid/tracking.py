"""
tracking.py

Person detection and tracking.
"""

import logging
from multiprocessing import Process
import cv2

logger = logging.getLogger(__name__)


def start_tracking(shared_dict):
    logger.info("Tracking starting up")
    shared_dict['hello'] = "hi"


class Tracking:
    def __init__(self, shared_dict):
        self.process = Process(target=start_tracking, args=(shared_dict,))
        self.process.start()

    def stop(self):
        self.process.terminate()
        self.process.join()

    def __del__(self):
        self.stop()
