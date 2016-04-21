"""
control.py

The Grid Control System

Hooks together the hardware interface, pattern modules, people tracking, and an
HTTP API for remote control.
"""

import sys
import time
try:
    from queue import Empty
    from imp import reload
except ImportError:
    from Queue import Empty
import signal
import logging
from multiprocessing import Manager, Queue
import numpy as np

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

        # Load available sinks
        self.sink = {}
        self.sinks = sinks.loaded_sinks
        sink_names = sorted(self.sinks.keys())
        logger.info("Available sinks: {}".format(sink_names))

        # Load available patterns
        self.pattern = None
        self.pattern_name = None
        self.patterns = patterns.loaded_patterns
        pattern_names = sorted(self.patterns.keys())
        logger.info("Available patterns: {}".format(pattern_names))

        # Start the tracking
        self.tracking_manager = Manager()
        self.tracking_dict = self.tracking_manager.dict()
        self.tracking = Tracking(self.tracking_dict)

        # Start the API
        self.cmd_queue = Queue()
        port, password = settings.API_PORT, settings.API_PASSWORD
        self.api = API(port, password, self.cmd_queue)

        # Set default legacy pattern colour
        self.legacycolour = (255, 255, 255)

        # Activate default sinks
        default_sinks = settings.DEFAULT_SINKS
        for sink in default_sinks:
            if sink in self.sinks:
                logger.info("Loading default sink %s", sink)
                self.sink[sink] = self.sinks[sink]()
            else:
                logger.error("Could not find default sink %s", sink)

    def main(self):
        while True:
            # Handle incoming API calls
            try:
                self.process_command(*self.cmd_queue.get_nowait())
            except Empty:
                pass

            if not self.pattern:
                continue

            # Run the pattern
            try:
                state, delay = self.pattern.update()
            except Exception:
                logger.exception("Exception in pattern %s",
                                 self.pattern_name)
                self._load_pattern(self.pattern_name)
                continue

            # To compensate for time taken to update sinks
            frametime = time.time()

            # Convert legacy monochrome patterns to colour:
            if state.shape == (7, 7):
                colourstate = np.zeros((7, 7, 3), dtype=np.uint8)
                for x in range(7):
                    for y in range(7):
                        if state[y][x]:
                            colourstate[y][x] = self.legacycolour
                        else:
                            colourstate[y][x] = (0, 0, 0)
                state = colourstate

            self._update_sinks(state)

            # Wait for next pattern frame
            sleeptime = delay - (time.time() - frametime)
            if sleeptime > 0.0:
                time.sleep(delay - (time.time() - frametime))
            else:
                logger.warning("Could not keep up with requested delay")

    def _update_sinks(self, state):
        if not self.sink:
            return
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

    def _cmd_list_commands(self, _):
        commands = ", ".join(x[5:] for x in dir(self) if x.startswith("_cmd_"))
        logger.info("Received LIST COMMANDS command.  Commands: {}".format(
            commands))

    def _cmd_stop(self, _):
        logger.info("Received STOP command, quitting")
        self.stop()

    def _cmd_load_pattern(self, pattern):
        logger.info("Received LOAD_PATTERN command for pattern %s", pattern)
        self._reload_patterns()
        if pattern in self.patterns.keys():
            self._load_pattern(pattern)
        else:
            logger.error("Could not find pattern %s", pattern)

    def _cmd_list_patterns(self, _):
        patterns = ", ".join(self.patterns.keys())
        logger.info("Received LIST_PATTERNS command.  Available patterns: {}"
                    "".format(patterns))

    def _cmd_list_sinks(self, _):
        sinks = ", ".join(self.sinks.keys())
        logger.info("Received LIST_SINK command.  Available sinks: {}"
                    "".format(sinks))

    def _reload_patterns(self):
        logger.info("Reloading patterns")
        self.patterns.clear()
        for mod in sys.modules:
            if mod.startswith("thegrid.patterns."):
                reload(sys.modules[mod])
        reload(sys.modules["thegrid.patterns"])
        self.patterns = sys.modules["thegrid.patterns"].loaded_patterns

    def _load_pattern(self, pattern):
        logger.info("Loading pattern {}".format(pattern))
        del self.pattern
        cls, cfg = self.patterns[pattern]
        self.pattern = cls(cfg, self.tracking)
        self.pattern_name = pattern

    def _cmd_set_legacy_colour(self, colour):
        self.legacycolour = tuple(map(int, colour.split(",")))

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
