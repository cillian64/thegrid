"""
thegrid.py

Pattern to the music of Daft Punk's "The Grid" from the soundtrack to Tron
Legacy.
"""

import logging
import numpy as np
from ..pattern import register_pattern, loaded_patterns
from .musicpattern import MusicPattern

logger = logging.getLogger(__name__)

@register_pattern("The Grid",
                  {"filename": "thegrid.wav",
                   "zeroth_beat": 9.979,
                   "align_beat": 80.5,
                   "align_beat_no": 120,
                   "beats_per_bar": 2})
class TheGrid(MusicPattern):
    def update(self):
        state = np.zeros((7,7), dtype=np.bool).flatten()
        state[:self.get_beat()%49] = True
        return state.reshape((7,7)), 0.1
        
