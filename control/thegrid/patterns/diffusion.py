"""
diffusion.py

Colour points diffuse through the grid.
"""

import logging
import numpy as np
from .pattern import Pattern, register_pattern
from colorsys import hsv_to_rgb
from numpy.random import randint
import sys

logger = logging.getLogger(__name__)


@register_pattern("Diffusion")
class Sample(Pattern):
    def __init__(self, cfg, tracking):
        logger.info("Diffusion pattern starting up")
        self.grid = np.zeros((7, 7, 3), dtype=int)
        self.n_points = 3
        self.reset()

    def isuniform(self):
        zeroed = self.grid[:, :] - self.grid[0, 0]
        return np.allclose(zeroed, np.zeros((7, 7, 3)))

    def reset(self):
        self.grid[:, :] = (0, 0, 0)
        for _ in range(self.n_points):
            rgb = hsv_to_rgb(np.random.random(), 1.0, 1.0)
            self.grid[randint(7), randint(7)] = [int(x*255) for x in rgb]

    def neighbours(self, x, y):
        points = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x+i >= 0 and x+i < 7 and
                    y+j >= 0 and y+j < 7):
                    points.append((y+j, x+i))
        return points

    def diffuse(self):
        for x in range(7):
            for y in range(7):
                neighbours = self.neighbours(x, y)
                for point in neighbours:
                    self.grid[y, x] += self.grid[point[1], point[0]]
                    self.grid[y, x] /= 2
                    self.grid[point[1], point[0]] = self.grid[y, x]

    def update(self):
        self.diffuse()
        if self.isuniform():
            self.reset()
        return self.grid, 1.0
