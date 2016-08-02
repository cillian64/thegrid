"""
Colour runner pattern

Looks as if a coloured pole is running through The Grid!  Imagine: grid is set
to all blue.  Suddenly, one of them is red, and the co-ordinates of the red
pole changes, leaving a fading red trail in its wake.  We call this moving red
pole the runner.  The colour of the runner changes, as does the background i
colour.  Exciting!
"""

import numpy as np
import logging
logger = logging.getLogger(__name__)

from ..pattern import Pattern, register_pattern


@register_pattern("[COLOUR] Runner")
class ColourRunner(Pattern):
    """Colour runner pattern"""

    def __init__(self, config, ui):
        super().__init__(config, ui)
        self.grid_gen = self.generate_grid()
        self.runner_loc = self.runner_location()

    def update(self):
        return next(self.grid_gen), 1/10

    @staticmethod
    def runner_location():
        """Yields (x, y) co-ordinates of the runner"""
        start = [0, 0]
        yield start

        loc = start
        while True:
            if loc[0] == 6:
                loc = [loc[0] - 1, loc[1]]
            else:
                loc = [loc[0] + 1, loc[1]]
            yield loc

    def generate_grid(self):
        """
        Yields 7x7x6 numpy array representing grid pole configurations

        Yields a 7x7x6 numpy array, with each entry representing the
        configuration of a pole in The Grid.
        """
        grid = np.zeros((7, 7, 6), dtype=np.uint8)
        while True:
            runner_x, runner_y = next(self.runner_loc)
            grid[runner_x][runner_y][0:3] = [255, 0, 0]
            yield grid
