"""
ayb.py

All your base are belong to us.
"""

import random
import logging
import numpy as np
from ...pattern import register_pattern, silent, clicker
from .musicpattern import MusicPattern
from colorsys import hsv_to_rgb

logger = logging.getLogger(__name__)


@register_pattern("[MUSIC] All Your Base",
                  {"filename": "thegrid/patterns/musicpatterns/ayb.wav",
                   "first_beat": 5.2,
                   "align_beat": 36.0,
                   "align_beat_no": 84,
                   "beats_per_bar": 4})
@silent()
class CaptainKirk(MusicPattern):
    def __init__(self, config, ui):
        self.state = np.zeros((7, 7, 3), dtype=np.uint8)
        self.state_persist = np.zeros((7, 7, 3), dtype=np.uint8)
        self.last_bar = 0
        self.last_beat = None
        super().__init__(config, ui)

    def update(self):
        bar, barbeat = self.get_barbeat()
        beat = self.get_beat()
        beat_portion = self.get_beat_portion()
#        logger.info("barbeat: {}, beat: {:03}".format(barbeat, beat))
        self.state[:] = 0

        if beat == 0:
            self.state[:, :] = (64, 0, 0)
        elif beat <= 20:
            if barbeat == 1:
                self.state[:3, :3] = (255, 0, 0)
            elif barbeat == 2:
                self.state[:3, 4:] = (255, 0, 0)
            elif barbeat == 3:
                self.state[4:, 4:] = (255, 0, 0)
            elif barbeat == 4:
                self.state[4:, :3] = (255, 0, 0)
        elif beat <= 36:
            if barbeat in (2, 4):
                self.state[:, :] = (255, 255, 0)
        elif beat <= 52:
            if barbeat in (2, 4):
                self.state[:, :] = (255, 255, 0)
            else:
                self.state[:, :] = (255, 0, 0)
        elif beat <= 56:
            if barbeat in (2, 4):
                self.state[:, 4:] = (255, 255, 0)
            else:
                self.state[:, :3] = (255, 0, 0)
        elif beat <= 60:
            if barbeat in (2, 4):
                self.state[:3, :] = (255, 255, 0)
            else:
                self.state[4:, :] = (255, 0, 0)
        elif beat <= 64:
            if barbeat in (2, 4):
                self.state[:, :3] = (255, 255, 0)
            else:
                self.state[:, 4:] = (255, 0, 0)
        elif beat <= 68:
            if barbeat in (2, 4):
                self.state[4:, :] = (255, 255, 0)
            else:
                self.state[:3, :] = (255, 0, 0)
        elif beat <= 76:
            if beat_portion <= 0.2:
                if barbeat in (1, 3):
                    self.state[:, :] = (255, 80, 0)
                else:
                    self.state[:, :] = (255, 255, 0)
        elif beat <= 84:
            if beat_portion <= 0.2:
                self.state[:, :] = (255, 255, 255)
        elif beat <= 100:
            for x in range(7):
                for y in range(7):
                    if barbeat in (1, 3):
                        if (x % 2) != (y % 2):
                            self.state[x, y] = (255, 0, 0)
                    else:
                        if (x % 2) == (y % 2):
                            self.state[x, y] = (255, 0, 0)
        elif beat <= 116:
            if barbeat == 1:
                for y in (0, 2, 4, 6):
                    for x in (0, 2, 4, 6):
                        self.state[y, x] = (255, 0, 0)
            elif barbeat == 2:
                for y in (0, 2, 4, 6):
                    for x in (1, 3, 5):
                        self.state[y, x] = (255, 0, 0)
            elif barbeat == 3:
                for y in (1, 3, 5):
                    for x in (1, 3, 5):
                        self.state[y, x] = (255, 0, 0)
            elif barbeat == 4:
                for y in (1, 3, 5):
                    for x in (0, 2, 4, 6):
                        self.state[y, x] = (255, 0, 0)
        elif beat <= 132: # orange fuzz
            for _ in range(10):
                self.state[np.random.randint(7), np.random.randint(7)] = (
                    np.random.randint(100, 256),
                    np.random.randint(100, 256), 0)
        elif beat <= 148: # Green fuzz
            for _ in range(10):
                self.state[np.random.randint(7), np.random.randint(7)] = (
                    0, np.random.randint(100, 256), 0)
        elif beat <= 164: # Cyan fuzz
            for _ in range(10):
                self.state[np.random.randint(7), np.random.randint(7)] = (
                    0, np.random.randint(100, 255),
                    np.random.randint(100, 256))
        elif beat <= 180: # Blue fuzz
            for _ in range(10):
                self.state[np.random.randint(7), np.random.randint(7)] = (
                    0, 0, np.random.randint(100, 256))
        elif beat <= 196: # Red striping
            col = int(beat_portion * 7)
            col = col if col <= 6 else 6
            self.state[:, col] = (255, 0, 0)
        elif beat <= 212: # Red reverse striping
            col = int(beat_portion * 7)
            col = 6 - col if col <= 6 else 0
            self.state[:, col] = (255, 0, 0)
        elif beat <= 228: # Red spinner
            if beat_portion < 0.25:
                self.state[:, 3] = (255, 0, 0)
            elif beat_portion <= 0.5:
                for i in range(7):
                    self.state[i, 6-i] = (255, 0, 0)
            elif beat_portion <= 0.75:
                self.state[3, :] = (255, 0, 0)
            else:
                for i in range(7):
                    self.state[i, i] = (255, 0, 0)
        elif beat <= 244: # Red reverse spinner
            if beat_portion < 0.25:
                self.state[:, 3] = (255, 0, 0)
            elif beat_portion <= 0.5:
                for i in range(7):
                    self.state[i, i] = (255, 0, 0)
            elif beat_portion <= 0.75:
                self.state[3, :] = (255, 0, 0)
            else:
                for i in range(7):
                    self.state[i, 6-i] = (255, 0, 0)
        elif beat <= 260: # Move zig! Flash blue/red
            if barbeat in (1, 3):
                self.state[:, :] = (0, 0, 255)
            else:
                self.state[:, :] = (255, 0, 0)
        elif beat <= 276: # Move zig! Flash green/yellow
            if barbeat in (1, 3):
                self.state[:, :] = (0, 255, 0)
            else:
                self.state[:, :] = (255, 255, 0)
        elif beat <= 292: # Move zig! Purple/yellow
            if barbeat in (1, 3):
                self.state[:, :] = (200, 0, 255)
            else:
                self.state[:, :] = (255, 255, 0)
        elif beat <= 308: # Move zig! White/black
            if barbeat in (1, 3):
                self.state[:, :] = (255, 255, 255)
        elif beat <= 340: # Interlude. Multicolour stepping and fade out
            if self.last_beat != beat:
                self.state_persist[:, :] = (0, 0, 0)
                for _ in range(20):
                    self.state_persist[np.random.randint(7),
                                       np.random.randint(7)] = (
                        np.random.randint(256), np.random.randint(256),
                        np.random.randint(256))
            self.state[:] = self.state_persist
            if beat >= 325:
                fade = 1 - (beat - 340) / 8
                faded = self.state * fade
                self.state[:] = faded
            self.last_beat = beat
                
        return self.state, 1.0/30

