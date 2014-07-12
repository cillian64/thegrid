"""
tracking.py

Person detection and tracking.
"""

import logging
from multiprocessing import Process

logger = logging.getLogger(__name__)

try:
    import cv2
except ImportError:
    logging.warning("Could not import cv2, continuing with no tracking")
    cv2 = None


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
