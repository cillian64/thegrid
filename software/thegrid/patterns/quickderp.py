import numpy as np
import logging
from ..pattern import Pattern, register_pattern
logger = logging.getLogger(__name__)


@register_pattern("[TEST] QuickDerp")
class Template(Pattern):
    mark = False

    def update(self):
        # Initialise an all-off silent grid
        grid = np.zeros((7, 7, 6), dtype=np.uint8)

        if self.mark:
            grid[:, :] = [20, 0, 0, 4, 0, 255]
            self.mark = False
        else:
            self.mark = True

        # Run again in 1/30 of a second, ie 30fps
        return grid, 1/30
