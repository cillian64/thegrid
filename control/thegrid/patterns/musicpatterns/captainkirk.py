"""
thegrid.py

Pattern to the music of Daft Punk's "The Grid" from the soundtrack to Tron
Legacy.
"""

import random
import logging
import numpy as np
from ..pattern import register_pattern, loaded_patterns
from .musicpattern import MusicPattern

logger = logging.getLogger(__name__)

def roll_without_wrap(a, shift, axis):
    temp = np.roll(a, shift, axis)
    if axis == 0 and shift > 0: # down
        temp[0, :] = False
    if axis == 0 and shift < 0: # up
        temp[-1, :] = False
    if axis == 1 and shift > 0: # right
        temp[:, 0] = False
    if axis == 1 and shift < 0: # left
        temp[:, -1] = False
    return temp


@register_pattern("CaptainKirk",
                  {"filename": "kirk.wav",
                   "first_beat": 0.8,
                   "align_beat": 45.0,
                   "align_beat_no": 100,
                   "beats_per_bar": 4})
class CaptainKirk(MusicPattern):
    def __init__(self, config, tracking):
        self.state = np.zeros((7,7), dtype=np.bool)
        self.last_bar = 0
        self.last_beat = 0
        super(TheGrid, self).__init__(config, tracking)

    def update(self):
        logger.info("{}, {}".format(self.get_barbeat(), self.get_beat()))
    
        if self.get_beat() > self.last_beat:
            print(self.get_beat())
            self.last_beat = self.get_beat()

        return numpy.zeros((7, 7, 3), dtype=np.uint8), 0.1
#
#        # Intro: sparkle
#        if self.get_beat() == 0:
#            state = np.zeros((7,7), dtype=np.bool).flatten()
#            state[random.randrange(0, 48)] = True
#            return state.reshape((7,7)), 0.05
#
#        # Talky bit: waves
#        if self.get_beat() < 15:
#            self.state = roll_without_wrap(self.state, 1, 1) # right
#            if self.get_bar() > self.last_bar:
#                self.last_bar += 1
#                if self.get_bar() % 2 == 0:
#                    self.state[:,0] = True
#            return self.state, 0.1
#
#        # Waves from 3 directions
#        if self.get_beat() == 15:
#            self.state = roll_without_wrap(self.state, -1, 0) # up
#            if self.get_beat() > self.last_beat:
#                self.state[-1, :] = True
#                self.last_beat = self.get_beat()
#            return self.state, 0.05
#        if self.get_beat() == 16:
#            self.state = roll_without_wrap(self.state, -1, 1) # left
#            if self.get_beat() > self.last_beat:
#                self.state[:, -1] = True
#                self.last_beat = self.get_beat()
#            return self.state, 0.05
#        if self.get_beat() == 17:
#            self.state = roll_without_wrap(self.state, 1, 0) # down
#            if self.get_beat() > self.last_beat:
#                self.state[0, :] = True
#                self.last_beat = self.get_beat()
#            return self.state, 0.05
#
#        if self.get_beat() >= 65:
#            self.state[:,:] = True
#            return self.state, 0.1
#
#        # Fallback
#        state = np.zeros((7,7), dtype=np.bool)
#        return state, 0.05
#        
