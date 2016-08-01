"""
Simple Pattern
"""

import numpy as np
import logging
from ..pattern import Pattern, register_pattern, monochrome, clicker
logger = logging.getLogger(__name__)


@register_pattern("Simple")
@clicker()
@monochrome((0, 0, 255))
class Simple(Pattern):
    i = 0

    def update(self):
        grid = np.zeros((7, 7), dtype=np.bool)
        grid[self.i, :] = 1
        self.i = (self.i + 1) % 7
        return grid, 1/7
