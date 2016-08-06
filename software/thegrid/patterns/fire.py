# A flame-like fireplace sort of effect.  Works by creating a nice flame
# coloured backdrop, and overlaying some black spots that move upwards to
# create a flame ripple effect.  Design borrowed from the OHM LED torches
# used on the EMF'16 DKs

import numpy as np
from math import sqrt, sin, cos, pi
from ..pattern import Pattern, register_pattern, silent
from colorsys import hsv_to_rgb

@register_pattern("[COLOUR] Fire")
@silent()
class PatternColourwave(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator()

    def generator(self):
        arr = np.zeros((7, 7, 3), dtype=np.uint8)
        base = np.zeros((7, 7, 3), dtype=np.uint8)
        blankers = np.zeros((7, 7), dtype=np.bool)
        # We want a nice smooth fade from white/pale yellow to yellow, to
        # orange, to red, to dark red.
        hue = np.linspace(1/6, 0, 7)
        sat = np.array((0.2, 0.5, 0.8, 1.0, 1.0, 1.0, 1.0))
        val = np.array((1.0, 1.0, 1.0, 1.0, 0.8, 0.6, 0.2))
        # Row 0 is the brightest, row 6 is the darkest.
        # Blankers start at row 0 and move up.
        
        hsv = list(zip(hue, sat, val))
        rgb = [[255*y for y in hsv_to_rgb(*x)] for x in hsv]
        for row in range(7):
            base[row, :] = rgb

        while True:
            # Scroll up the blankers
            for row in range(6, 0, -1):
                blankers[row, :] = blankers[row - 1, :]
            blankers[0, :] = False

            # If we have too few blacks spots in blankers, create one 
            if np.sum(blankers) < 30:
                blankers[0, np.random.randint(7)] = True
                blankers[0, np.random.randint(7)] = True

            # Update grid
            arr[:] = base
            arr[blankers.T] = (0, 0, 0)
            yield arr, 1.0/15

    def update(self):
        return self.gen.__next__()

