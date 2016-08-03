# Several coloured spotlights sweep around thegrid.  When they intersect
# the colours are summed

import numpy as np
from math import sqrt, sin, cos, pi
from ..pattern import Pattern, register_pattern, clicker
from colorsys import hsv_to_rgb

@register_pattern("[COLOUR] Spotlights")
@clicker()
class PatternColourwave(Pattern):
    def __init__(self, cfg, tracking):
        n_spots = 3
        self.spots = []
        for _ in range(n_spots):
            self.spots.append({})
        for spot in self.spots:
            # Set a colour with a random hue, full sat and value.  Scale up to
            # 0-255 then truncate to integer.
            spot['colour'] = hsv_to_rgb(np.random.rand(), 1.0, 1.0)
            spot['colour'] = [int(x*255) for x in spot['colour']]
            # Turn the colour tuple into a numpy array with correct dtype:
            spot['colour'] = np.array(spot['colour'], dtype=np.uint8)

            # Set a random start centrepoint within thegrid:
            spot['x'] = int(np.random.rand() * 7)
            spot['y'] = int(np.random.rand() * 7)

            # Set a velocity with a fixed magnitude and random angle:
            v_mag = 0.05
            angle = np.random.rand() * 2 * pi
            spot['vx'] = cos(angle) * v_mag
            spot['vy'] = sin(angle) * v_mag

            # Fixed radius for now:
            spot['r'] = 2

        self.arr = np.zeros((7, 7, 3), dtype=np.uint8)
        self.updaterate = 0.03


    def soft_set_point(self, target, colour):
        """Change a point in a numpy matrix to a new colour.
        But do it slowly and subtley.  If it doesn't already match the new
        colour, move it a small step towards the new colour so it fades
        gradually."""
        rate = 0.5
        if target[0] != colour[0]:
            target[0] += (colour[0] - target[0]) * rate
        if target[1] != colour[1]:
            target[1] += (colour[1] - target[1]) * rate
        if target[2] != colour[2]:
            target[2] += (colour[2] - target[2]) * rate

    def add_capped(self, dest, src):
        """Add each element in two vectors, but cap the result at 255 if it
           would otherwise be greater."""
        for i in range(dest.size):
            if src[i] + dest[i] > 255:
                dest[i] = 255
            else:
                dest[i] += src[i]
            

    def update(self):

        self.arr[:, :] = (0, 0, 0)
        for x in range(7):
            for y in range(7):
                target_colour = np.zeros((3,))
                for spot in self.spots:
                    d = self.is_in_circle(spot['x'], spot['y'], spot['r'],
                                         x, y)
                    if d is not None:
                        self.add_capped(target_colour,
                                        spot['colour']*(1-d/spot['r']))
                self.soft_set_point(self.arr[x, y], target_colour)

        for spot in self.spots:
            # Simple bouncing ball model.  However we set the boundaries at
            # one position outside of thegrid so we get a bit more room to
            # bounce!
            spot['x'] += spot['vx']
            spot['y'] += spot['vy']
            if spot['x'] < spot['r'] - 1 or spot['x'] > 8 - spot['r']:
                spot['vx'] *= -1
            if spot['y'] < spot['r'] - 1 or spot['y'] > 8 - spot['r']:
                spot['vy'] *= -1

        return self.arr, self.updaterate


    def is_in_circle(self, xc, yc, radius, x, y):
        """
        Work out if the point (x, y) is contained within a circle centred
        on (xc, yc) with radius radius.  If it is, return the distance from
        the centrepoint.  If not, return None
        """
        d = sqrt((x - xc)**2 + (y - yc)**2)
        return d if d < radius else None

