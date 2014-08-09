"""
on.py

A simple sample pattern to turn on all the channels. Useful for load-testing
"""

import logging
import numpy as np
from .pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)


@register_pattern("On")
class Sample(Pattern):
    def update(self):
        logger.info("Updating pattern")
        return np.ones((7, 7), dtype=np.bool), 0.1
