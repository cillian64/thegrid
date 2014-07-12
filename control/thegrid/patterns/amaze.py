"""
amaze.py

aMAZE, the multiplayer light maze
"""

import logging
import numpy as np
from .pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)


@register_pattern("aMAZE (1P)", {"players": 1})
@register_pattern("aMAZE (2P)", {"players": 2})
class AMaze(Pattern):
    def __init__(self, config, tracking):
        logger.info("aMAZE initialised")

    def update():
        return np.zeros((7, 7), dtype=np.bool)
