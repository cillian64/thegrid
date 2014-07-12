"""
tracking.py

Person detection and tracking.
"""

from multiprocessing import Process
import cv2

def start_tracking(shared_dict):
    shared_dict['hello'] = "hi";

class Tracking:
    def __init__(self, shared_dict):
        self.process = Process(target=start_tracking, args=(shared_dict,))
        self.process.start()
    
    def stop(self):
        self.process.terminate()
        self.process.join()

    def __del__(self):
        self.stop()
