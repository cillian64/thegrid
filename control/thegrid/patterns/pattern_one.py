# Pattern for the grid

import numpy as np
from .pattern import Pattern, register_pattern

grid_size = 7

@register_pattern("PatternScan")
class PatternScan(Pattern):
    count = 0

    def update(self):
        lights = np.zeros((7,7), dtype=np.bool)

        for i in range(7):
            if (self.count & (1 << i)):
                lights[i][i] = 1

        self.count+=1

        if (self.count >= 128):
            self.count = 0

        # Return, get called again in 100ms
        delay = 0.1
        return lights, delay

@register_pattern("PatternSpin")
class PatternSpin(Pattern):
    count = 0
    phase = 0

    def update(self):
        lights = np.zeros((7,7), dtype=np.bool)

        if self.phase == 0: # Up the y axis
            lights[0][self.count] = 1
        elif self.phase == 1: # Across the top
            lights[self.count][grid_size-1] = 1
        elif self.phase == 2: # Down the side
            lights[grid_size-1][(grid_size-1)-self.count] = 1
        elif self.phase == 3: # Back accross the bottom
            lights[(grid_size-1)-self.count][0] = 1

        self.count+=1

        # Move the self.count
        if self.count >= grid_size:
            self.count = 0
            self.phase+=1

            # Move through the self.phases
            if self.phase >= 4:
                self.phase = 0

        # Return, get called again in 100ms
        delay = 0.1
        return lights, delay
