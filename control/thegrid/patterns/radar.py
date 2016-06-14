# HSV demo pattern.  Displays a grid of HSV points, all with full value.
# Hue varies in the X axis, saturation in the Y axis.

import numpy as np
from .pattern import Pattern, register_pattern

grid_size = 7

@register_pattern("Radar")
class PatternColourwheel(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator()

    def generator(self):
        lights = np.zeros((7,7, 3), dtype=np.uint8)
        targets = [(1, 1), (5, 5)]
        beam_angle = 0.0

        empty_decay_rate = 20
        target_decay_rate = int(empty_decay_rate / 4)

        while True:
            for x in range(7):
                for y in range(7):
                    # Draw the beam sweep:
                    angle = np.arctan2((y - 3.0), (x - 3.0)) + np.pi
                    lag = beam_angle - angle
                    if lag < 0:
                        lag += 2*np.pi
                    if lag < 2*np.pi*10/360:
                        if (x, y) in targets:
                            lights[y, x, 1] = 255.0
                        else:
                            lights[y, x, 1] = 150.0

                    if (x, y) in targets:
                        decay_rate = target_decay_rate
                    else:
                        decay_rate = empty_decay_rate

                    if lights[y, x, 1] >= decay_rate:
                        lights[y, x, 1] -= decay_rate
                    else:
                        lights[y, x, 1] = 0

                    if lights[y, x, 1] > 200:
                        q = lights[y, x, 1] - 200
                        q *= 2
                        lights[y, x, 0] = q
                        lights[y, x, 2] = q
                    else:
                        lights[y, x, 0] = 0
                        lights[y, x, 2] = 0

            lights[3, 3, 1] = 255
            yield lights, 0.03
            beam_angle += 0.1 # Sweep speed
            if beam_angle > 2*np.pi:
                beam_angle -= 2*np.pi

    def update(self):
        return self.gen.__next__()

