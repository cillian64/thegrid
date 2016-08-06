"""
static_pattern.py

Playlist of cool static patterns.
"""
from __future__ import division
import os
import logging
import numpy as np
from ...pattern import Pattern, register_pattern, clicker

logger = logging.getLogger(__name__)


class BlockParseError(RuntimeError):
    pass


def extract_blocks(lines):
    block = []
    for line in lines:
        block.append(line)
        if len(block) == 9:
            if block[0] != "\n":
                logger.error("Block started with <%s>", repr(block[0]))
                raise BlockParseError("Blocks must start with a blank line")
            try:
                delay = int(block[-1])
            except ValueError:
                logger.error("Block ended with <%s>", block[-1])
                raise BlockParseError("Blocks must end with an integer")
            rows = []
            for row in block[1:8]:
                if row[-1] != "\n":
                    logger.error("Row ended in <%s>", row[-1])
                    raise BlockParseError("Row didn't end in a newline.")
                row = row[:-1]
                if len(row) != 7:
                    logger.error("Row was %d characters", len(row))
                    raise BlockParseError("Rows must only be 7 characters")
                for char in row:
                    if char not in (".", "*", "r", "R", "g", "G", "b", "B"):
                        logger.error("Row contained <%s>", char)
                        raise BlockParseError("Rows may only have `.`, `*`, "
                                              "`r`, `R`, `g`, `G`, `b`, `B`")
                rows.append(row)
            yield rows, delay
            block = []
    if block != []:
        raise BlockParseError("Last block malformed")


@register_pattern("[MONOCHROME] Rectangles", {"file": "rectangles.txt"})
@register_pattern("[MONOCHROME] Smile", {"file": "smile.txt"})
@register_pattern("[MONOCHROME] Spinner", {"file": "spinner.txt"})
@register_pattern("[MONOCHROME] Wave", {"file": "wave.txt"})
@register_pattern("[MONOCHROME] Zoom", {"file": "zoom.txt"})
@register_pattern("[MONOCHROME] Zoomout", {"file": "zoomout.txt"})
@register_pattern("[COLOUR] Spin", {"file": "colourspin.txt"})
@register_pattern("[COLOUR] Zoom", {"file": "colourzoom.txt"})
@clicker()
class StaticPattern(Pattern):
    def __init__(self, config, tracking):
        basepath = os.path.normpath(
            os.path.join(os.path.abspath(__file__), os.pardir))
        filepath = os.path.join(basepath, config["file"])

        logger.info("Loading playlist file {}".format(filepath))
        try:
            f = open(filepath)
        except IOError:
            logger.error("Playlist file not found!")
            self.blocks = None
            self.block = None
            return

        # Print title
        title = next(f).strip()
        logger.info("Playlist: {}".format(title))

        # Load blocks:
        self.blocks = list(extract_blocks(f))
        logger.info("Loaded {0} frames".format(len(self.blocks)))

        if self.blocks == []:
            logger.warn("No frames loaded!")
            self.block = None
            self.blocks = None

        self.block = 0
        self.arr = np.zeros((7, 7, 3), dtype=np.uint8)

    def update(self):
        if self.blocks is None or self.block is None:
            logger.warn("No frames available!")
            return self.arr, 1

        curblock = self.blocks[self.block]
        self.block += 1
        self.block %= len(self.blocks)

        for y, row in enumerate(curblock[0]):
            for x, col in enumerate(row):
                if col == '*' or col == 'w' or col == 'W':
                    self.arr[y, x] = (100, 100, 100)
                elif col == 'r' or col == 'R':
                    self.arr[y, x] = (100, 0, 0)
                elif col == 'g' or col == 'G':
                    self.arr[y, x] = (0, 100, 0)
                elif col == 'b' or col == 'B':
                    self.arr[y, x] = (0, 0, 100)
                else:
                    self.arr[y, x] = (0, 0, 0)

        sleep = curblock[1] / 1000
        return self.arr, sleep
