"""
console.py

Visualise grid output state on an console terminal.
"""

import logging
from .sink import Sink, register_sink

logger = logging.getLogger(__name__)


@register_sink("Console")
class Console(Sink):
    def __init__(self):
        logger.info("Console sink initialised")

    def update(self, state):
        pass
