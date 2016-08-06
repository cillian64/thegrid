"""
captainkirk.py

Captain Kirk is climbing a mountain. Why is he climbing a mountain?
"""

import random
import logging
import numpy as np
from ...pattern import register_pattern, silent
from .musicpattern import MusicPattern
from colorsys import hsv_to_rgb

logger = logging.getLogger(__name__)


@register_pattern("[MUSIC] Shatner of the Mount",
                  {"filename": "thegrid/patterns/musicpatterns/kirk.wav",
                   "first_beat": 0.8,
                   "align_beat": 45.0,
                   "align_beat_no": 95.5,
                   "beats_per_bar": 4})
@silent()
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
#        logger.info("barbeat: {}, beat: {:03}".format(barbeat, beat))
        self.state[:] = 0

        # Intro:
        # Red stepping
        if beat >= 1 and beat <= 32:
            self.state[:] = 0
            self.state[5, int(barbeat)] = (255, 0, 0)

        # Lyrics start:
        # Red stepping with yellow pulse
        elif beat >= 33 and beat <= 60:
            self.state[5, int(barbeat)] = (255, 0, 0)
            if barbeat in (2, 4) and beat_portion < 0.2:
                self.state[:, 0] = (255, 255, 0)
                self.state[:, 6] = (255, 255, 0)

        # Breakdown before chorus: yellow pulse solo
        elif beat >= 61 and beat <= 64:
            if barbeat in (2, 4) and beat_portion < 0.2:
                self.state[:, 0] = (255, 255, 0)
                self.state[:, 6] = (255, 255, 0)

        # First half of chorus - red/orange/yellow fuzz
        elif beat >= 65 and beat <= 96:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (np.random.randint(200, 256),
                                    np.random.randint(0, 256),
                                    np.random.randint(0, 40))

        # Second half of chorus: variety of coloured fuzz per bar
        elif beat >= 97 and beat <= 104: # Pink/purple
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (np.random.randint(128, 256),
                                    0,
                                    np.random.randint(128, 256))
        elif beat >= 105 and beat <= 112: # Blue/cyan
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (0,
                                    np.random.randint(128, 256),
                                    np.random.randint(128, 256))
        elif beat >= 113 and beat <= 120: # Shades of green:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (0,
                                    np.random.randint(32, 256),
                                    0)
        elif beat >= 121 and beat <= 124: # Shades of grey:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                level = np.random.randint(64, 128)
                self.state[x, y] = (level, level, level)
        elif beat >= 125 and beat <= 128: # White fuzz
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                level = 255
                self.state[x, y] = (level, level, level)

        # Back to the verse -- 4 steps around the outside of a square
        elif beat >= 129 and beat <= 144:
            self.state[1, barbeat] = (255, 0, 0)
            self.state[5, 6 - barbeat] = (255, 0, 0)

        # More verse.
        # Now pulse the outside of the square on the offbeat and
        # the inside of the square on the on-beat
        elif beat >= 145 and beat <= 152:
            self.state[1, barbeat + 1] = (255, 0, 0)
            self.state[5, 6 - barbeat] = (255, 0, 0)
            if barbeat in (1, 3) and beat_portion < 0.2:
                self.state[2:5, 2:5] = (255, 255, 0)
            if barbeat in (2, 4) and beat_portion < 0.2:
                self.state[0:7, 0] = (255, 255, 0)
                self.state[0:7, 6] = (255, 255, 0)
                self.state[0, 0:7] = (255, 255, 0)
                self.state[6, 0:7] = (255, 255, 0)

        # Kirk is on the mountain. Checkerboard effect.
        elif beat >= 153 and beat <= 156:
            if barbeat == 1:
                self.state[:, :] = (255, 0, 0)
            elif barbeat == 2:
                self.state[:3, :] = (255, 0, 0)
            elif barbeat == 3:
                self.state[:3, :3] = (255, 0, 0)
                self.state[4:, 4:] = (255, 0, 0)
            elif barbeat == 4:
                for x in (0, 2, 4, 6):
                    for y in (0, 2, 4, 6):
                        self.state[x, y] = (255, 0, 0)
        elif beat >= 157 and beat <= 160:
            if barbeat in (1, 3):
                for x in (1, 3, 5):
                    for y in (1, 3, 5):
                        self.state[x, y] = (255, 0, 0)
            else:
                for x in (0, 2, 4, 6):
                    for y in (0, 2, 4, 6):
                        self.state[x, y] = (255, 0, 0)

        # Some more verse.  Spinner effect with varying colour.
        elif beat >= 161 and beat <= 176:
            if beat >= 161 and beat <= 168:
                colour = (255, 0, 0)
            else:
                colour = (255, 128, 0)

            if barbeat == 1:
                self.state[1:6, 3] = colour
            elif barbeat == 2:
                for i in range(1, 6):
                    self.state[i, 6-i] = colour
            elif barbeat == 3:
                self.state[3, 1:6] = colour
            elif barbeat == 4:
                for i in range(1, 6):
                    self.state[i, i] = colour

        # Some more verse.  Spinner effect with outer flash
        elif beat >= 177 and beat <= 188:
            if barbeat == 1:
                self.state[1:6, 3] = (255, 255, 0)
            elif barbeat == 2:
                for i in range(1, 6):
                    self.state[i, i] = (255, 255, 0)
            elif barbeat == 3:
                self.state[3, 1:6] = (255, 255, 0)
            elif barbeat == 4:
                for i in range(1, 6):
                    self.state[i, 6-i] = (255, 255, 0)
            if barbeat in (2, 4) and beat_portion < 0.2:
                self.state[0:7, 0] = (255, 0, 0)
                self.state[0:7, 6] = (255, 0, 0)
                self.state[0, 0:7] = (255, 0, 0)
                self.state[6, 0:7] = (255, 0, 0)

        # Dark patch in the bar 189-193, with two flashes in the last beat:
        elif beat == 192:
            if ((beat_portion >= 0.0 and beat_portion <= 0.2)
                or (beat_portion >= 0.5 and beat_portion <= 0.7)):
                self.state[:, :] = (255, 255, 255)

        # God there's more verse.  Okay let's do some zoomout/pyramids.
        elif beat >= 193 and beat <= 224:
            if beat >= 193 and beat <= 196:
                colour = (255, 0, 0)
            elif beat >= 197 and beat <= 200:
                colour = (255, 128, 0)
            elif beat >= 201 and beat <= 204:
                colour = (255, 255, 0)
            elif beat >= 205 and beat <= 208:
                colour = (128, 255, 0)
            elif beat >= 209 and beat <= 212:
                colour = (0, 255, 0)
            elif beat >= 213 and beat <= 216:
                colour = (0, 255, 255)
            elif beat >= 217 and beat <= 220:
                colour = (0, 128, 255)
            else:
                colour = (0, 0, 255)
                barbeat = 5 - barbeat # lol switcheroo!

            if barbeat == 1:
                self.state[3, 3] = colour
            elif barbeat == 2:
                self.state[2, 2:5] = colour
                self.state[4, 2:5] = colour
                self.state[3, 2] = colour
                self.state[3, 4] = colour
            elif barbeat == 3:
                self.state[1, 1:6] = colour
                self.state[5, 1:6] = colour
                self.state[1:6, 1] = colour
                self.state[1:6, 5] = colour
            else: # barbeat == 4
                self.state[0, 0:7] = colour
                self.state[6, 0:7] = colour
                self.state[0:7, 0] = colour
                self.state[0:7, 6] = colour

        # Chorus! Phew.  Multicolour fuzz for a while
        # First, blue fuzz <3
        elif beat >= 225 and beat <= 232:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (0, 0, np.random.randint(64, 256))
        # Now cyan:
        elif beat >= 233 and beat <= 240:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (0,
                                    np.random.randint(128, 256),
                                    np.random.randint(128, 256))
        # Now blue/green:
        elif beat >= 241 and beat <= 248:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (0,
                                    np.random.randint(0, 256),
                                    np.random.randint(0, 256))

        # Penultimately grey for half a bar:
        elif beat >= 249 and beat <= 252:
            for _ in range(10):
                level = np.random.randint(64, 196)
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y, :] = level

        # Finally white.
        elif beat >= 253 and beat <= 256:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                self.state[x, y] = (255, 255, 255)

        # More chorus.  Let's have some random fully saturated fuzz:
        elif beat >= 257 and beat <= 288:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                rgb = hsv_to_rgb(np.random.rand(), 1.0, 1.0)
                self.state[x, y] = [int(255*x) for x in rgb]

        # Yet more chorus.  For the finale let's have fully saturated fuzz
        # with overlayed full white spinner.
        elif beat >= 289 and beat <= 304:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                rgb = hsv_to_rgb(np.random.rand(), 1.0, 1.0)
                self.state[x, y] = [int(200*x) for x in rgb]
            if beat_portion < 0.25:
                self.state[3, :] = (255, 255, 255)
            elif beat_portion < 0.5:
                for n in range(7):
                    self.state[n, 6-n] = (255, 255, 255)
            elif beat_portion < 0.75:
                self.state[:, 3] = (255, 255, 255)
            else:
                for n in range(7):
                    self.state[n, n] = (255, 255, 255)

        # More chorus.  Now fully saturated fuzz overlayed with white zoomout
        elif beat >= 305 and beat <= 315:
            for _ in range(10):
                x, y = np.random.randint(0, 7, (2,))
                rgb = hsv_to_rgb(np.random.rand(), 1.0, 1.0)
                self.state[x, y] = [int(200*x) for x in rgb]
            if beat_portion < 0.25:
                self.state[3, 3] = (255, 255, 255)
            elif beat_portion < 0.5:
                self.state[2, 2:5] = (255, 255, 255)
                self.state[4, 2:5] = (255, 255, 255)
                self.state[3, 2] = (255, 255, 255)
                self.state[3, 4] = (255, 255, 255)
            elif beat_portion < 0.75:
                self.state[1, 1:6] = (255, 255, 255)
                self.state[5, 1:6] = (255, 255, 255)
                self.state[1:6, 1] = (255, 255, 255)
                self.state[1:6, 5] = (255, 255, 255)
            else:
                self.state[0, 0:7] = (255, 255, 255)
                self.state[6, 0:7] = (255, 255, 255)
                self.state[0:7, 0] = (255, 255, 255)
                self.state[0:7, 6] = (255, 255, 255)

        # Outro - blinking centre pole
        elif beat >= 316 and beat <= 320:
            if beat_portion < 0.2:
                self.state[3, 3] = (255, 255, 255)

        else:
            self.state[:, :] = (0, 0, 0)
#            print("Stop!")

        return self.state, 1.0/30

