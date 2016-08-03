"""
Colour runner pattern

Looks as if a coloured pole is running through The Grid!  Imagine: grid is set
to all blue.  Suddenly, one of them is red, and the co-ordinates of the red
pole changes, leaving a fading red trail in its wake.  We call this moving red
pole the runner.  The colour of the runner changes, as does the background
colour.  Exciting!
"""

import collections
import copy
import itertools
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
        return next(self.grid_gen), 1/5

    @staticmethod
    def runner_location():
        """Yields (x, y) co-ordinates of the runner"""
        x_length_cycle = itertools.cycle((list(range(7)) +
                                          list(reversed(range(7)))))
        y_length_cycle = copy.deepcopy(x_length_cycle)
        x, y = 0, next(y_length_cycle)
        yield x, y

        while True:
            for _ in range(7):
                yield (next(x_length_cycle), y)
            y = next(y_length_cycle)

    @staticmethod
    def interpolate_rgb(start_rgb, end_rgb, distance, n=7):
        return [int(start_rgb[channel] + distance/n
                * (end_rgb[channel] - start_rgb[channel]))
                for channel in range(3)]

    def generate_grid(self):
        """
        Yields 7x7x6 numpy array representing grid pole configurations

        Yields a 7x7x6 numpy array, with each entry representing the
        configuration of a pole in The Grid.
        """
        blue = [0, 0, 255]
        red = [255, 0, 0]

        wake = collections.deque(maxlen=7)
        wake.appendleft(next(self.runner_loc))

        grid = np.zeros((7, 7, 6), dtype=np.uint8)
        grid[:, :] = blue + [0, 0, 0]

        while True:
            runner_x, runner_y = wake[0]
            print()
            logger.info('runner_x, runner_y = {0}, {1}'.format(runner_x,
                                                               runner_y))
            grid[runner_x][runner_y][0:3] = red
            yield grid

            for i in range(len(wake)):
                x, y = wake[i]
                logger.info('x, y = {0}, {1}'.format(x, y))
                grid[x][y][0:3] = self.interpolate_rgb(red, blue, i)
                logger.info(grid[x][y][0:3])
            wake.appendleft(next(self.runner_loc))
