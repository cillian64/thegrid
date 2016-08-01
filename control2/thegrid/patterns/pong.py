"""
pong.py

A two player pong clone on TheGrid.
"""

import logging
import numpy as np
from ..pattern import Pattern, register_pattern, monochrome, clicker

logger = logging.getLogger(__name__)


@register_pattern("[INTERACTIVE] Pong1P", {"players": 1})
@register_pattern("[INTERACTIVE] Pong2P", {"players": 2})
@clicker()
@monochrome()
class Pong(Pattern):
    def __init__(self, config, tracking):
        logger.info("Pong initialised")
        logger.info("Pong config: {}".format(config))
        self.config = config
        self.tracking = tracking
        self.ball = [0, 0]
        self.ballv = [2, 1]

    def update(self):
        self.ball[0] += self.ballv[0]
        self.ball[1] += self.ballv[1]
        if self.ball[0] >= 6:
            self.ballv[0] = -self.ballv[0]
        if self.ball[0] <= 0:
            self.ballv[0] = -self.ballv[0]
        if self.ball[1] >= 6:
            self.ballv[1] = -self.ballv[1]
        if self.ball[1] <= 0:
            self.ballv[1] = -self.ballv[1]

        grid = np.zeros((7, 7), dtype=np.bool)
        grid[self.ball[1], self.ball[0]] = True

        logger.info("about to return, grid.shape=%s", grid.shape)
        return grid, 0.5
