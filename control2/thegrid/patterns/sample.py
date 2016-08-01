"""
sample.py

A simple sample pattern to demonstrate the API.
"""

import logging
import numpy as np
from ..pattern import Pattern, register_pattern, clicker

logger = logging.getLogger(__name__)


@register_pattern("[COLOUR] Example Pattern")
@clicker()
class Sample(Pattern):
    def __init__(self, cfg, ui):
        self.gen = self.generator()

    def generator(self):
        logger.info("Updating pattern")
        grid = np.zeros((7, 7, 3), dtype=np.uint8)

        while True:
            grid[:, :] = (0, 0, 0) # Set the whole grid to black
            # Set gridsquare row 0 column 0:
            grid[0, 0] = (255, 0, 0)  # Red, in RGB colour code
            yield grid, 1.0 # Display this grid for one second

            grid[:, :] = (0, 0, 0)
            grid[0, 1] = (0, 255, 0)  # Set row 0 col 1 to green
            yield grid, 1.0

            grid[:, :] = (0, 0, 0)
            grid[2, 1] = (0, 0, 255)
            yield grid, 1.0

            grid[:, :] = (255, 255, 255)
            yield grid, 0.2


    def update(self):
        return self.gen.__next__()

