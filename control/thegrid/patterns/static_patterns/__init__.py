"""
static_pattern.py

Playlist of cool static patterns.
"""

import os
import logging
import numpy as np
from ..pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)


class BlockParseError(RuntimeError):
    pass


def extract_blocks(lines):
    block = []
    for line in lines:
        block.append(line)
        if len(block) == 9:
            if block[0] != "\n":
                raise BlockParseError("Blocks must start with a blank line")
            try:
                delay = int(block[-1])
            except ValueError:
                raise BlockParseError("Blocks must end with an integer")
            rows = []
            for row in block[1:8]:
                if row[-1] != "\n":
                    raise BlockParseError("Row didn't end in a newline.")
                row = row[:-1]
                if len(row) != 7:
                    raise BlockParseError("Rows must only be 7 characters")
                for char in row:
                    if char not in (".", "*"):
                        raise BlockParseError("Rows may only have `.` or `*`")
                rows.append(row)
            yield rows, delay
            block = []
    if block != []:
        raise BlockParseError("Last block malformed")


@register_pattern("Rectangles", {"file": "rectangles.txt"})
@register_pattern("Smile", {"file": "smile.txt"})
@register_pattern("Spinner", {"file": "spinner.txt"})
@register_pattern("Wave", {"file": "wave.txt"})
@register_pattern("Zoom", {"file": "zoom.txt"})
@register_pattern("Zoomout", {"file": "zoomout.txt"})
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
        title = next(f)
        logger.info("Playlist: {}".format(title))

        # Load blocks:
        self.blocks = list(extract_blocks(f))
        logger.info("Loaded {0} frames".format(len(self.blocks)))

        if self.blocks == []:
            logger.warn("No frames loaded!")
            self.block = None
            self.blocks = None

        self.block = 0

    def update(self):
        if self.blocks is None or self.block is None:
            logger.warn("No frames available!")
            return np.zeros((7, 7), dtype=np.bool), 1

        curblock = self.blocks[self.block]
        self.block += 1
        self.block %= len(self.blocks)

        frame = np.array([list(l) for l in curblock[0]]) == '*'
        sleep = curblock[1] / 1000
        return frame, sleep
