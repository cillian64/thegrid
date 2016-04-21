"""
sample.py

A simple sample pattern to demonstrate the API.
"""

import logging
import numpy as np
from .pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)


@register_pattern("Sample")
class Sample(Pattern):
    def update(self):
        logger.info("Updating pattern")
        grid = np.zeros((7, 7, 3), dtype=np.uint8)
        grid[0][0][0] = 255
        grid[0][1][1] = 255
        grid[0][2][2] = 255
        return grid, 1
