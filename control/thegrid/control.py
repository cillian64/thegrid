"""
control.py

The Grid Control System

Hooks together the hardware interface, pattern modules, people tracking, and an
HTTP API for remote control.
"""

import sys
import time
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

        self.sink = {}
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

        default_sinks = settings.DEFAULT_SINKS
        for sink in default_sinks:
            if sink in self.sinks:
                logger.info("Loading default sink %s", sink)
                self.sink[sink] = self.sinks[sink]()
            else:
                logger.error("Could not find default sink %s", sink)

    def main(self):
        while True:
            try:
                self.process_command(*self.cmd_queue.get_nowait())
            except queue.Empty:
                pass

            if self.pattern:
                try:
                    state, delay = self.pattern.update()
                except Exception:
                    logger.exception("Exception in pattern %s", self.pattern)
                    logger.error("Unloading pattern")
                    del self.pattern
                    self.pattern = None

                frametime = time.time()

                self._update_sinks(state)

                sleeptime = delay - (time.time() - frametime)
                if sleeptime > 0.0:
                    time.sleep(delay - (time.time() - frametime))
                else:
                    logger.warning("Could not keep up with requested delay")

    def _update_sinks(self, state):
        if self.sink:
            for sink in self.sink:
                try:
                    self.sink[sink].update(state)
                except Exception:
                    logger.exception("Exception in sink %s", sink)
                    logger.error("Reloading sink")
                    cls = type(self.sink[sink])
                    del self.sink[sink]
                    self.sink[sink] = cls()
                    logger.info("Reloaded sink %s", sink)

    def process_command(self, cmd, val):
        cmdfun = "_cmd_{}".format(cmd)
        if hasattr(self, cmdfun):
            getattr(self, cmdfun)(val)
        else:
            logger.error("Unknown command %s received", cmd)

    def _cmd_stop(self, _):
        logger.info("Received STOP command, quitting")
        self.stop()

    def _cmd_load_pattern(self, pattern):
        logger.info("Received LOAD_PATTERN command for pattern %s", pattern)
        if pattern in self.patterns.keys():
            logger.info("Loading pattern {}".format(pattern))
            del self.pattern
            cls, cfg = self.patterns[pattern]
            self.pattern = cls(cfg, self.tracking)
        else:
            logger.error("Could not find pattern %s", pattern)

    def _cmd_load_sink(self, sink):
        logger.info("Received LOAD_SINK command for sink %s", sink)
        if sink in self.sinks.keys() and sink not in self.sink:
            logger.info("Loading sink {}".format(sink))
            self.sink[sink] = self.sinks[sink]()
        elif sink not in self.sinks.keys():
            logger.error("Could not find sink %s", sink)
        elif sink in self.sink:
            logger.warning("Sink %s already loaded", sink)

    def _cmd_unload_sink(self, sink):
        logger.info("Received UNLOAD_SINK command for sink %s", sink)
        if sink in self.sink:
            logger.info("Unloading sink %s", sink)
            del self.sink[sink]
        else:
            logger.warning("Sink %s was not loaded", sink)

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
