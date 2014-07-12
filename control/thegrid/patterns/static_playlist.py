"""
static_playlist.py

Playlist of cool static patterns.
"""

import logging
import os
import numpy as np
from .pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)


def fussyreadline(f):
    line = f.readline()
    if line == '':
        return None  # EOF
    line = line.rstrip()
    if line == '':
        return line  # Pass on blank lines
    if line[0] == '#':  # Comment!
        return fussyreadline(f)
    return line


@register_pattern("Rectangles", {"file": "rectangles.txt"})
@register_pattern("Smile", {"file": "smile.txt"})
@register_pattern("Sparkle", {"file": "sparkle.txt"})
@register_pattern("Spinner", {"file": "spinner.txt"})
@register_pattern("Wave", {"file": "wave.txt"})
@register_pattern("Zoom", {"file": "zoom.txt"})
@register_pattern("Zoomout", {"file": "zoomout.txt"})
class Sample(Pattern):
    def __init__(self, config, tracking):
        curpath = os.path.normpath(
            os.path.join(os.path.abspath(__file__), os.pardir))
        basepath = os.path.join(curpath, "static_patterns")
        filename = os.path.join(basepath, config["file"])
        logger.info("Loading playlist file: "+filename)
        try:
            f = open(filename)
        except FileNotFoundError:
            logger.error("Playlist file not found!")
            self.blocks = None
            self.block = None
            return
        # Print title:
        title = f.readline().rstrip()
        logger.info("Playlist: "+title)

        # Skip description
        line = f.readline().rstrip()
        while line != '':
            line = f.readline().rstrip()

        # Load blocks:
        self.blocks = []
        line = fussyreadline(f)
        while line is not None:  # None is EOF
            block = []
            while line != '' and line is not None:
                if len(block) != 7 and len(line) != 7:
                    logger.error("Incorrect line length, block {}, line {}".
                        format(len(self.blocks)+1, len(block)+1))
                else:
                    block.append(line)
                line = fussyreadline(f)

            if len(block) != 8:
                logger.error("Incorrect block length, block {}".
                    format(len(self.blocks)+1))
            else:
                self.blocks.append(block)

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
        if self.block >= len(self.blocks):
            self.block = 0

        sleep = float(curblock[7]) / 1000
        curblock = [list(line) for line in curblock[:7]]
        
        return np.array(curblock) == '*', sleep

