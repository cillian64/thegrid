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
@clicker()
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



        return self.state, 1.0/30

