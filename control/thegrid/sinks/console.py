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
        for _ in range(0, 9):
            print("")

    def update(self, state):
        print("\033[9A\r", end='')
        for row in state:
            a = list(map(lambda x: '#' if x else '.', list(row)))
            a = ' '.join(a)
            print(a)
        print("")
