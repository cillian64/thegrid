"""
leonardo.py

Hardware sink to sen dcurrent grid state to the shift registers using an
Arduino Leonardo running the leonardo.ino sketch.
"""

import logging
logger = logging.getLogger(__name__)

try:
    import serial
except ImportError:
    logger.warning("Could not import Serial, aborting leonardo sink")
    serial = None
else:
    from serial.serialutil import SerialException

from .sink import Sink, register_sink



@register_sink("Leonardo")
class Leonardo(Sink):
    def __init__(self):
        if serial is not None:
            try:
                self.ser = serial.Serial("/dev/ttyACM0", 115200)
            except SerialException:
                logger.error("Problem initialising Leonardo serial link:")
                logger.error("Check the Leonardo is plugged in")
                logger.error("and that /dev/ttyACM0 exists.")
                self.ser = None
            else:
                logger.info("Leonardo sink initialised")
        else:
            self.ser = None
            logger.error("Can't initialise leonardo sink, no Serial library")

    def update(self, state):
        if self.ser is None:
            return

        output = bytearray([2, 0, 0, 0, 0, 0, 0, 0, 3])
        for colidx, column in enumerate(state.T):
            tot = 0
            for rowidx, bit in enumerate(column):
                tot += bit * (64 // 2**rowidx) # invert again.
            output[7-colidx] = tot # invert because it seems inverted...
        try:
            self.ser.write(output)
        except OSError:
            logger.error("Error writing to serial port - Leonardo has")
            logger.error("probably been unplugged.  Disabling serial port.")
            self.ser = None

