"""
ftdi.py

Hardware sink to send current grid state to the shift registers using an
FT232RL chip in bitbang mode.
"""

import logging
from pylibftdi import BitBangDevice
from .sink import Sink, register_sink

logger = logging.getLogger(__name__)


@register_sink("FTDI")
class FTDI(Sink):
    def __init__(self):
        self.device = BitBangDevice()
        # We use pins 0, 1 and 4 as RCK, SRCK, DATA
        self.device.direction = (1 << 0) | (1 << 1) | (1 << 4)
        logger.info("Hardware sink initialised")

    def update(self, state):
        for column in state.T:
            for idx, bit in enumerate(column):
                if bit:
                    # Cause SRCK to rise while asserting DATA
                    self.device.port = (1 << 4)
                    self.device.port = (1 << 4) | (1 << 1)
                else:
                    # Cause SRCF to rise while not asserting DATA
                    self.device.port = 0
                    self.device.port = 0 | (1 << 1)

        # RCK
        self.device.port = 1
        self.device.port = 0
