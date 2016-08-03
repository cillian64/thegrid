"""
playlist.py

A pattern of patterns. We must go deeper.
"""

import time
import logging
from ..pattern import Pattern, register_pattern, loaded_patterns

logger = logging.getLogger(__name__)


playlists = {
    "[MONOCHROME] Cool Patterns": [
        ("[MONOCHROME] Lightning", 120),
        ("[MONOCHROME] On", 20),
        ("[MONOCHROME] Sparkle", 20),
        ("[MONOCHROME] Rectangles", 60),
        ("[MONOCHROME] Wave", 100),
        ("[MONOCHROME] Zoom", 30),
        ("[MONOCHROME] Zoomout", 30),
        ("[MONOCHROME] Zoom", 30),
        ("[MONOCHROME] Zoomout", 30),
        ]}

class Playlist(Pattern):
    def __init__(self, playlist, tracking):
        for entry in playlist:
            # Test that each item can be instantiated with its config.
            # Any errors thrown here will be caught early.
            logger.info("Test initialising %s", entry[0])
            cls, cfg = loaded_patterns[entry[0]]
            cls(cfg, tracking).update()

        self.playlist = playlist
        self.tracking = tracking

        self.time = 0
        self.entry_idx = len(self.playlist) - 1

    def update(self):
        #logger.info("time - self.time is: %f", time.time() - self.time)
        #logger.info("pattern time is: %d", self.playlist[self.entry_idx][1])
        if time.time() - self.time > self.playlist[self.entry_idx][1]:
            self.entry_idx += 1
            self.entry_idx %= len(self.playlist)
            logger.info("Playlist advancing to entry %d", self.entry_idx)
            cls, cfg = loaded_patterns[self.playlist[self.entry_idx][0]]
            self.child = cls(cfg, self.tracking)
            self.time = time.time()
        return self.child.update()

for name, playlist in playlists.items():
    register_pattern(name, playlist)(Playlist)
