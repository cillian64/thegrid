# HSV demo pattern.  Displays a grid of HSV points, all with full value.
# Hue varies in the X axis, saturation in the Y axis.

import numpy as np
from ..pattern import Pattern, register_pattern, clicker
from colorsys import hsv_to_rgb

grid_size = 7

@register_pattern("[COLOUR] Wheel")
class PatternColourwheel(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator()

    def generator(self):
        state = np.zeros((7, 7, 6), dtype=np.uint8)
        lights = np.zeros((7, 7, 3), dtype=np.uint8)
        colour_offset = 0.0

        while True:
            for x in range(7):
                for y in range(7):
                    radius = np.sqrt((y - 3.0)**2 + (x - 3.0)**2)
                    angle = np.arctan2((y - 3.0), (x - 3.0)) + np.pi
                    hue = angle / (2.0 * np.pi) + colour_offset
                    sat = radius / np.sqrt(2*3.0**2)
                    
                    rgb = hsv_to_rgb(hue, 1.0, 1.0 - sat)
                    lights[y, x] = (rgb[0]*255, rgb[1]*255, rgb[2]*255)
            lights[3, 3] = (0, 0, 0)
            state[:, :, :3] = lights
            yield state, 1.0/30
            colour_offset += 0.01
            if colour_offset > 2.0*np.pi:
                colour_offset -= 2.0*np.pi

    def update(self):
        return self.gen.__next__()

