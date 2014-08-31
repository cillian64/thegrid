import time
import logging
import numpy as np
from .pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)

@register_pattern("SimpleCV")
class SimpleCV(Pattern):
    def __init__(self, config, tracking):
        self.lit = {}
        self.config = config
        self.tracking = tracking
    def update(self):
        grid = np.zeros((7, 7), dtype=np.bool)
        for centroid in self.tracking.data['centroids']:
            x = max(0, min(6, int(round(centroid[0]))))
            y = max(0, min(6, int(round(centroid[1]))))
            logger.info("centroid={},{} grid={},{}".format(
                centroid[0], centroid[1], x, y))
            self.lit[(y, 6-x)] = time.time()
        for k in self.lit:
            if time.time() - self.lit[k] < 5:
                y, x = k
                grid[y][x] = True
        return grid, 0.1
