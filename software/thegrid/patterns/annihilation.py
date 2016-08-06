"""TOTAL ANNIHILATION"""

import itertools
import numpy as np
import logging
logger = logging.getLogger(__name__)

from ..pattern import Pattern, register_pattern


@register_pattern("[COLOUR] Annihiliation")
class ColourAnnihilation(Pattern):
    """
    Colour annihilation pattern

    Rainbow rows will move towards each other from opposite sides of The Grid.
    When the collide, they will turn white, and white rows of decreasing
    brightness will emanate from the collision. !
    """

    def __init__(self, config, ui):
        super().__init__(config, ui)
        self.grid_gen = self.generate_grid()

    def update(self):
        return next(self.grid_gen), 1/5

    @staticmethod
    def colour_gradient(n=3):
        """
        Returns list of rainbow colours in gradient.

        Returns a list of colours gradating from red to green to blue to red.
        Kwarg n is the number of interpolation steps between each colour.
        """
        red = [255, 0, 0]
        green = [0, 255, 0]
        blue = [0, 0, 255]

        start_rgb_cycle = itertools.cycle([red, green, blue])
        end_rgb_cycle = itertools.cycle([green, blue, red])

        colours = []
        for _ in range(3):
            start_rgb = next(start_rgb_cycle)
            end_rgb = next(end_rgb_cycle)
            for i in range(n):
                rgb = [int(start_rgb[channel] +
                       i/n * (end_rgb[channel] - start_rgb[channel]))
                       for channel in range(3)]
                colours.append(rgb)
        return colours

    def generate_grid(self):
        """
        Yields 7x7x6 numpy array representing grid pole configurations

        Yields a 7x7x6 numpy array, with each entry representing the
        configuration of a pole in The Grid.
        """
        rainbow = np.concatenate((np.array(self.colour_gradient()[0:7]),
                                  np.zeros((7, 3), dtype=np.uint8)), 1)
        grid = np.zeros((7, 7, 6), dtype=np.uint8)

        for i, j in zip([0, 1, 2], [6, 5, 4]):
            grid[:, :] = [0 for _ in range(6)]
            grid[:, i] = rainbow
            grid[:, j] = rainbow
            yield grid
        grid[:, :] = [0 for _ in range(6)]
        grid[:, 3] = [255, 255, 255, 0, 0, 0]
        yield grid
