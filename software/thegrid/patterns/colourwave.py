# Waves move across the grid in random directions, with random colours.
# Waves move in arbitrary angular directions.

# Coding-wise, the way we do this is to have a rectangle which moves around in
# real-space.  At each update, after moving this rectangle appropriately, we
# check for each grid-pole whether it lies inside the rectangle.  If it does,
# we set that grid-pole to the rectangle's colour.  If not, we set that pole
# to the background colour.
# For simplicity, in real-space we shift so that the centre of the grid is
# the point (0, 0).  This means the centre of the rectangle moves along lines
# which intersect (0, 0).  We convert to thegrid's discrete 0-6,0-6 axes when
# doing the per-pole evaluation.

import numpy as np
from math import sqrt, sin, cos, pi
from ..pattern import Pattern, register_pattern
from colorsys import hsv_to_rgb

@register_pattern("[COLOUR] Wave")
class PatternColourwave(Pattern):
    def __init__(self, cfg, tracking):
        self.rectlength = 2.0 * sqrt(2) * 7 + 1 # Theoretical max length is 
                                              # thegrid's hypotenues.  Add a 
                                              # bit for safety.
        self.rectwidth = 3.2  # Three gridpoles plus a bit.
        self.rectspeed = 0.1 # One unit per update
        self.updaterate = 1.0/30 # Time delay between updates, in seconds.

        self.arr = np.zeros((7, 7, 6), dtype=np.uint8)
        self.new_wave()


    def new_wave(self):
        # Bearing in maths angles: 0 is "right" and +ve is ACW. In radians.
        self.wavedir = np.random.rand() * 2*pi
        # Rotate -10,0 by theta to find the new start point
        self.rectx = -10.0*cos(self.wavedir)
        self.recty = -10.0*sin(self.wavedir)

#        self.bgcolour = hsv_to_rgb(np.random.rand(), np.random.rand(), 0.1)
#        self.bgcolour = [int(255.0*x) for x in self.bgcolour]
        self.bgcolour = (0, 0, 0)

        self.rectcolour = hsv_to_rgb(np.random.rand(), # Hue
                                     0.5 + 0.5*np.random.rand(), # Saturation
                                     1.0) # Value
        self.rectcolour = [int(255.0*x) for x in self.rectcolour]

#        print("New wave, angle={:.1f} degrees".format(
#            self.wavedir/2/pi*360))

    def soft_set_point(self, target, colour):
        """Change a point in a numpy matrix to a new colour.
        But do it slowly and subtley.  If it doesn't already match the new
        colour, move it a small step towards the new colour so it fades
        gradually."""
        rate = 0.02
        if target[0] != colour[0]:
            target[0] += (colour[0] - target[0]) * rate
        if target[1] != colour[1]:
            target[1] += (colour[1] - target[1]) * rate
        if target[2] != colour[2]:
            target[2] += (colour[2] - target[2]) * rate

        # Now set the sound part.
        if sum(colour[:3]) == 0:
            volume = int(sum(target[:3]))
        else:
            volume = int(200 * sum(target[:3]) / sum(colour[:3]))
        target[3] = 4 # Noise
        target[4] = 0 # noise freq doesn't matter
        target[5] = volume


    def update(self):
        # First let's update the rectangle centre.
        self.rectx += self.rectspeed * cos(self.wavedir)
        self.recty += self.rectspeed * sin(self.wavedir)
#        print("Rect centre: {}".format((self.rectx, self.recty)))

        # Check if we need to start a new wave:
        # Rotate rect centre by -theta and see if this lies past +10
        xp = self.rectx*cos(-self.wavedir) - self.recty*sin(-self.wavedir)
        if xp > 10.0:
            self.new_wave()

        for x in range(7):
            for y in range(7):
                if self.is_in_rect(self.rectx, self.recty, self.wavedir,
                                   self.rectlength, self.rectwidth, x, y):
                    self.soft_set_point(self.arr[x, y], self.rectcolour)
                else:
                    self.soft_set_point(self.arr[x, y], self.bgcolour)

        return self.arr, self.updaterate


    def is_in_rect(self, xc, yc, theta, l, w, x, y):
        """For working out whether a gridpole falls in the rectangle, we
        do a coordinate rotation:
        xnew = xold.cos(theta) - yold.sin(theta)
        ynew = xold.sin(theta) + yold.cos(theta)
        Since theta is the rectangle movement direction, we can rotate by
        -theta to get back to our normal orthogonal axes.

        So we take our trial point x,y, subtract the centre point so that
        the centre of the rectangle becomes 0,0, then rotate by -theta.
        Then we can check if -l/2 < x < l/2 && -w/2 < y < w/2"""

        # First normalise our point so gridpole 3,3 becomes the centre at
        # 0,0
        x = x - 3
        y = 3 - y  # y is inverted because grid has +ve=down but normal
                   # geometry has +ve=up
        # Now subtract the rectangle centre so it becomes 0,0
        x -= xc
        y -= yc
        xp = x*cos(-theta) - y*sin(-theta)
        yp = x*sin(-theta) + y*cos(-theta)
        return (xp > -w/2 and xp < w/2 and yp > -l/2 and yp < l/2)
