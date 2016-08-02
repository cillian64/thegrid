"""
Colour ripple pattern

Colours will rippple from the centre of The Grid, with the colour changing
gradually through the spectrum.  Pretty!  Hopefully.
"""

import collections
import copy
import numpy as np
import logging
from ..pattern import Pattern, register_pattern
logger = logging.getLogger(__name__)


@register_pattern("ColourRipple")
class ColourRipple(Pattern):
    """
    Colour ripple pattern

    Colours will emanate from the centre of the grid, with colour moving
    gradually through the spectrum.
    """

    def __init__(self, config, ui):
        super().__init__(config, ui)
        self.grid_gen = self.generate_grid()

    @staticmethod
    def colour_gradient(n=100):
        """Yields deque containing four RGB tuples."""
        colours = collections.deque(maxlen=4)
        for _ in range(4):
            colours.appendleft(tuple([255, 255, 255]))

        while True:
            start_rgb = [0, 0, 0]
            for channel in range(3):
                end_rgb = [0, 0, 0]
                end_rgb[channel] = 255

                for i in range(n):
                    rgb = copy.deepcopy(start_rgb)
                    rgb[channel] = int(start_rgb[channel] + i/n *
                                       (end_rgb[channel] - start_rgb[channel]))
                    colours.appendleft(tuple(rgb))
                    yield colours
                start_rgb = rgb

    def update(self):
        """Return a tuple of (new_grid, update_time)"""
        return next(self.grid_gen), 1/50

    def generate_grid(self):
        colour_gradient = self.colour_gradient()
        grid = np.zeros((7, 7, 6), dtype=np.uint8)

        while True:
            colours = copy.deepcopy(next(colour_gradient))
            grid[3][3] = colours.popleft() + (0, 0, 0)

            for i, j in zip([2, 1, 0], [4, 5, 6]):
                c = colours.popleft()
                grid[:, i] = c + (0, 0, 0)
                grid[:, j] = c + (0, 0, 0)
                grid[i, :] = c + (0, 0, 0)
                grid[j, :] = c + (0, 0, 0)

            yield grid
