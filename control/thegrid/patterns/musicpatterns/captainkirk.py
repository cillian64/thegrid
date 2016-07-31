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
                   "align_beat_no": 95,
                   "beats_per_bar": 4})
class CaptainKirk(MusicPattern):
    def __init__(self, config, tracking):
        self.state = np.zeros((7, 7, 3), dtype=np.uint8)
        self.last_bar = 0
        self.last_beat = 0
        super(CaptainKirk, self).__init__(config, tracking)

    def update(self):
        bar, barbeat = self.get_barbeat()
        beat = self.get_beat()
        beat_portion = self.get_beat_portion()
#        logger.info("barbeat: {}, beat: {:03}".format(barbeat, beat))
        self.state[:] = 0

        # Intro:
        # Red stepping
        if beat >= 1 and beat <= 32:
            print("Step {}".format(barbeat))
            self.state[:] = 0
            self.state[5, int(barbeat)] = (255, 0, 0)

        # Lyrics start:
        # Red stepping with yellow pulse
        if beat >= 33 and beat <= 60:
            print("Step and pulse: {}".format(barbeat))
            self.state[5, int(barbeat)] = (255, 0, 0)
            if barbeat in (2, 4) and beat_portion < 0.2:
                self.state[:, 0] = (255, 255, 0)
                self.state[:, 6] = (255, 255, 0)

        # Breakdown before chorus: yellow pulse solo
        if beat >= 61 and beat <= 64:
            print("Pulse: {}".format(barbeat))
            if barbeat in (2, 4) and beat_portion < 0.2:
                self.state[:, 0] = (255, 255, 0)
                self.state[:, 6] = (255, 255, 0)

        # First half of chorus - red/orange/yellow fuzz
        if beat >= 65 and beat <= 96:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (np.random.randint(200, 256),
                                    np.random.randint(0, 256),
                                    np.random.randint(0, 40))

        # Second half of chorus: variety of coloured fuzz per bar
        if beat >= 97 and beat <= 104: # Pink/purple
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (np.random.randint(128, 256),
                                    0,
                                    np.random.randint(128, 256))
        if beat >= 105 and beat <= 112: # Blue/cyan
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (0,
                                    np.random.randint(128, 256),
                                    np.random.randint(128, 256))
        if beat >= 113 and beat <= 120: # Shades of green:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (0,
                                    np.random.randint(32, 256),
                                    0)
        if beat >= 121 and beat <= 124: # Shades of grey:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                level = np.random.randint(64, 128)
                self.state[x, y] = (level, level, level)
        if beat >= 125 and beat <= 128: # White fuzz
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                level = 255
                self.state[x, y] = (level, level, level)

        if beat >= 129:
            print("Stop!")

    
#        if self.get_beat() > self.last_beat:
#            print(self.get_beat())
#            self.last_beat = self.get_beat()

        if beat < 95:
            return self.state, 1.0
        else:
            return self.state, 0.1
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
