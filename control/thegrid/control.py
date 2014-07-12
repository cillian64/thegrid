"""
control.py

The Grid Control System

Hooks together the hardware interface, pattern modules, people tracking, and an
HTTP API for remote control.
"""

import sys
import queue
import signal
import logging
from multiprocessing import Manager, Queue

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")

from . import settings
from .api import API
from .tracking import Tracking
from . import patterns
from . import sinks


logger = logging.getLogger("thegrid.control")


class Control:
    def __init__(self, settings):
        logger.info("The·Grid Control starting up")
        self.settings = settings

        self.sink = None
        self.sinks = sinks.loaded_sinks
        sink_names = sorted(self.sinks.keys())
        logger.info("Available sinks: {}".format(sink_names))

        self.pattern = None
        self.patterns = patterns.loaded_patterns
        pattern_names = sorted(self.patterns.keys())
        logger.info("Available patterns: {}".format(pattern_names))

        self.tracking_manager = Manager()
        self.tracking_dict = self.tracking_manager.dict()
        self.tracking = Tracking(self.tracking_dict)

        self.cmd_queue = Queue()
        port, password = settings.API_PORT, settings.API_PASSWORD
        self.api = API(port, password, self.cmd_queue)

    def main(self):
        while True:
            try:
                self.process_command(*self.cmd_queue.get_nowait())
            except queue.Empty:
                pass

            if self.pattern:
                state = self.pattern.update()
                if self.sink:
                    self.sink.update(state)

    def process_command(self, cmd, val):
        logger.info("Received command: ({}, {})".format(cmd, val))
        if cmd == "stop":
            logger.info("Received STOP command, quitting")
            self.stop()
        if cmd == "load_pattern":
            logger.info("Received LOAD_PATTERN command")
            if val in self.patterns.keys():
                logger.info("Loading pattern {}".format(val))
                del self.pattern
                cls, cfg = self.patterns[val]
                self.pattern = cls(cfg, self.tracking)
        if cmd == "load_sink":
            logger.info("Received LOAD_SINK command")
            if val in self.sinks.keys():
                logger.info("Loading sink {}".format(val))
                del self.sink
                self.sink = self.sinks[val]()

    def stop(self):
        logger.info("Control is now terminating")
        if self.tracking:
            self.tracking.stop()
        if self.api:
            self.api.stop()
        sys.exit(0)

    def _signal(self, sig, frame):
        if sig == signal.SIGINT:
            logger.info("Received SIGINT, quitting")
            self.stop()

if __name__ == "__main__":
    control = Control(settings)
    signal.signal(signal.SIGINT, control._signal)
    control.main()
