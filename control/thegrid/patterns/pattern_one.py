# Pattern for the grid

import numpy as np
from .pattern import Pattern, register_pattern

grid_size = 7

@register_pattern("PatternScan")
class PatternScan(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator()

    def generator(self):
        lights = np.zeros((7,7), dtype=np.bool)
        while True:
            for count in range(128):
                lights[:][:] = 0
                for i in range(7):
                    if (count & (1 << i)):
                        lights[i][i] = 1
                yield lights, 0.1

    def update(self):
        return self.gen.__next__()

@register_pattern("PatternSpin")
class PatternSpin(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator()

    def update(self):
        return self.gen.__next__()

    def generator(self):
        lights = np.zeros((7,7), dtype=np.bool)
        delay = 0.1
        while True:
            for count in range(7): # phase 0, up y axis
                lights[:][:] = 0
                lights[0][count] = 1
                yield lights, delay

            for count in range(7): # phase 1, across top
                lights[:][:] = 0
                lights[count][6] = 1
                yield lights, delay

            for count in range(7): # phase 2, down side
                lights[:][:] = 0
                lights[6][6 - count] = 1
                yield lights, delay

            for count in range(7): # phase 3, back across bottom
                lights[:][:] = 0
                lights[6 - count][0] = 1
                yield lights, delay

