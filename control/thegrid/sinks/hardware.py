"""
hardware.py

Hardware sink to send current grid state to the shift registers.
"""

import logging
from .sink import Sink, register_sink

logger = logging.getLogger(__name__)


@register_sink("Hardware")
class Hardware(Sink):
    def __init__(self):
        logger.info("Hardware sink initialised.")

    def update(self, state):
        pass
