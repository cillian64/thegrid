"""
musicpattern.py

The base class for patterns set to music, for other musical patterns to inherit
from.
"""

import logging
logger = logging.getLogger(__name__)

try:
    import pyglet
except ImportError:
    print("Could not import pyglet, music patterns won't be available")
from ..pattern import Pattern
from math import floor

class MusicPattern(Pattern):
    def __init__(self, config, tracking):
        self.setup_bpm(config)
        filename = config["filename"]
        logger.info("Loading %s", filename)
        self.musicfile = pyglet.resource.media(filename, streaming=False)
        logger.info("Starting player")
        self.musicplayer = self.musicfile.play()

    def __del__(self):
        self.musicplayer.delete()
        self.musicfile.delete()

    def setup_bpm(self, config):
        self.first_beat = config["first_beat"]
        self.bps = ((config["align_beat"] - config["first_beat"]) /
                    config["align_beat_no"])
        self.beats_per_bar = config["beats_per_bar"]

    def barbeat_to_t(self, bar, beat):
        return self.beat(bar*self.beats_per_bar + beat)

    def beat_to_t(self, beat):
        return self.first_beat + self.bps * beat

    def t_to_beat(self, t):
        beat = (t - self.first_beat) // self.bps
        return beat+1 if beat >= 0 else 0

    def t_to_barbeat(self, t):
        bar = (self.t_to_beat(t) - 1) // self.beats_per_bar + 1
        beat = self.t_to_beat(t) % self.beats_per_bar 
        if beat == 0:
            beat = self.beats_per_bar
        return (bar, beat)

    def get_time(self):
        return self.musicplayer.time

    def get_beat(self):
        return self.t_to_beat(self.get_time())

    def get_bar(self):
        return self.t_to_barbeat(self.get_time())[0]

    def get_barbeat(self):
        return self.t_to_barbeat(self.get_time())

