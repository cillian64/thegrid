import numpy as np
import logging
from ..pattern import Pattern, register_pattern
logger = logging.getLogger(__name__)


@register_pattern("[TEST] Sound")
class SoundTest(Pattern):
    def __init__(self, config, ui):
        self.i = 0

    def update(self):
        # Initialise an all-off silent grid
        grid = np.zeros((7, 7, 6), dtype=np.uint8)

        if self.i == 0:
            grid[0, 0] = [0, 255, 0, 1, 0, 255]
        elif self.i == 1:
            grid[0, 0] = [0, 255, 0, 0, 255, 255]
        elif self.i == 2:
            grid[0, 0] = [0, 255, 0, 2, 0, 255]
        elif self.i == 3:
            grid[0, 0] = [0, 255, 0, 0, 255, 255]
        elif self.i == 4:
            grid[0, 0] = [0, 255, 0, 3, 0, 255]
        elif self.i == 5:
            grid[0, 0] = [0, 255, 0, 0, 255, 255]
        elif self.i == 6:
            grid[0, 0] = [0, 255, 0, 4, 255, 255]
        elif self.i == 7:
            grid[0, 0] = [0, 255, 0, 0, 255, 255]
        elif self.i == 8:
            grid[0, 0] = [0, 255, 0, 5, 255, 255]
        elif self.i == 9:
            grid[0, 0] = [0, 255, 0, 0, 255, 255]

        self.i = (self.i + 1) % 10

        return grid, 1/2
