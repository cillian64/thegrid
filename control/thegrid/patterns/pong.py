"""
pong.py

A two player pong clone on TheGrid.
"""

import logging
import numpy as np
from .pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)


@register_pattern("Pong (1P)", {"players": 1})
@register_pattern("Pong (2P)", {"players": 2})
class Pong(Pattern):
    def __init__(self, config, tracking):
        logger.info("Pong initialised")

    def update():
        return np.zeros((7, 7), dtype=np.bool)
