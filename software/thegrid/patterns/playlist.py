"""
playlist.py

A pattern of patterns. We must go deeper.
"""

import time
import logging
from ..pattern import Pattern, register_pattern, loaded_patterns

logger = logging.getLogger(__name__)


playlists = {
    "[PLAYLIST] Cool Patterns": [
        ("[MONOCHROME] Lightning", 120),
        ("[MONOCHROME] On", 20),
        ("[MONOCHROME] Sparkle", 20),
        ("[MONOCHROME] Rectangles", 60),
        ("[MONOCHROME] Wave", 100),
        ("[MONOCHROME] Zoom", 30),
        ("[MONOCHROME] Zoomout", 30),
        ("[MONOCHROME] Zoom", 30),
        ("[MONOCHROME] Zoomout", 30),
    ],
    "[TEST] Stopping Playlist": [
        ("[TEST] Stopping Red", 30),
        ("[TEST] Stopping Grn", 30),
        ("[TEST] Stopping Blu", 30),
    ],
    "[PLAYLIST] Colour Patterns": [
        ("[COLOUR] Ripple", 60),
        ("[COLOUR] Spin", 15),
        ("[COLOUR] Game of Life", 180),
        ("[COLOUR] Rainbow Runner", 60),
        ("[COLOUR] Ripple", 60),
        ("[COLOUR] Zoom", 20),
        ("[MONOCHROME] Sparkle", 30),
        ("[COLOUR] Wave", 180),
        ("[COLOUR] Diffusion", 120),
        ("[COLOUR] Radar (Moving)", 60),
        ("[COLOUR] Snake", 60),
        ("[COLOUR] Spotlights", 60)
    ]
}


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
        if time.time() - self.time > self.playlist[self.entry_idx][1]:
            self._advance_playlist()
        try:
            return self.child.update()
        except StopIteration:
            self._advance_playlist()
            return self.child.update()

    def _advance_playlist(self):
        self.entry_idx += 1
        self.entry_idx %= len(self.playlist)
        logger.info("Playlist advancing to entry %d", self.entry_idx)
        cls, cfg = loaded_patterns[self.playlist[self.entry_idx][0]]
        self.child = cls(cfg, self.tracking)
        self.time = time.time()

for name, playlist in playlists.items():
    register_pattern(name, playlist)(Playlist)
