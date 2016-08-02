"""
sparkle.py

Cool sparkley effect
"""

import logging
import numpy as np
from random import random, randrange

from ..pattern import Pattern, register_pattern, monochrome, clicker

logger = logging.getLogger(__name__)


@register_pattern("[MONOCHROME] Sparkle", {'flashlen': 0.05,
                                           'delaylen': 0.5})
@clicker()
@monochrome()
class Sample(Pattern):
    def __init__(self, config, tracking):
        self.flashlen = config['flashlen']
        self.delaylen = config['delaylen']
        self.flashing = False

    def update(self):
        field = np.zeros((7, 7), dtype=np.bool)

        if self.flashing:
            self.flashing = False
            return field, random()*self.delaylen
        else:
            x = randrange(0, 7)
            y = randrange(0, 7)
            field[y][x] = True

            self.flashing = True
            return field, self.flashlen

