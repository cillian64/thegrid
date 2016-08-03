"""
Template Pattern

Copy this file to your new pattern file and modify as described below.
"""

import numpy as np
import logging
from ..pattern import Pattern, register_pattern
logger = logging.getLogger(__name__)


# The register_pattern decorator causes this pattern to be added to the list,
# with an optional config which is saved as `self.config`.
# You can add the decorator multiple times if you want to register the same
# code with different names/configs.
@register_pattern("[TEST] Stopping Red", (255, 0, 0))
@register_pattern("[TEST] Stopping Grn", (0, 255, 0))
@register_pattern("[TEST] Stopping Blu", (0, 0, 255))
class Stopping(Pattern):
    def update(self):
        if hasattr(self, "done"):
            raise StopIteration
        grid = np.zeros((7, 7, 6), dtype=np.uint8)
        grid[:, :] = self.config + (0, 0, 0)
        self.done = True
        return grid, 1
