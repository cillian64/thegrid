"""
sample.py

A simple sample pattern to demonstrate the API.
"""

import logging
import numpy as np
from .pattern import Pattern, register_pattern

logger = logging.getLogger(__name__)


@register_pattern("Sample")
class Sample(Pattern):
    def update():
        logger.info("Updating pattern")
        return np.zeros((7, 7), dtype=np.bool)
