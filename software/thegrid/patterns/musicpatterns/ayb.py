"""
ayb.py

All your base are belong to us.
"""

import random
import logging
import numpy as np
from ...pattern import register_pattern, clicker
from .musicpattern import MusicPattern
from colorsys import hsv_to_rgb

logger = logging.getLogger(__name__)


@register_pattern("[MUSIC] All Your Base",
                  {"filename": "thegrid/patterns/musicpatterns/ayb.wav",
                   "first_beat": 5.2,
                   "align_beat": 36.7,
                   "align_beat_no": 84,
                   "beats_per_bar": 4})
@clicker(vol=0)
class CaptainKirk(MusicPattern):
    def __init__(self, config, ui):
        self.state = np.zeros((7, 7, 3), dtype=np.uint8)
        self.last_bar = 0
        self.last_beat = 0
        super().__init__(config, ui)

    def update(self):
        bar, barbeat = self.get_barbeat()
        beat = self.get_beat()
        beat_portion = self.get_beat_portion()
        logger.info("barbeat: {}, beat: {:03}".format(barbeat, beat))
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



        return self.state, 1.0/30

