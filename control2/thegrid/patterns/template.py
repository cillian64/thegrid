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
@register_pattern("Template")
@register_pattern("TemplateWithConfig", {"colour": (0, 255, 0)})
class Template(Pattern):
    """
    This class will have self.config set from the register_pattern argument,
    and self.ui set as a reference to the global UI helper.
    If you override __init__(), please call super().__init__().
    """

    def update(self):
        """
        The update() method is called by the main control loop on a time basis
        you can specify. You should compute the new grid state in this method.

        The grid shape is specified by a (7, 7, 6) numpy array of type uint8,
        with the first two dimensions specifying the (x, y) pole coordinate,
        and the third dimension giving (red, green, blue, sound type, sound
        frequency, sound volume).

        Sound types:
            0: silent
            1: sine
            2: square
            3: triangle
            4: noise
            5: click

        Sound frequencies and volumes range 0-255 and are scaled in hardware to
        meet the available sounder response.

        The time until next update is specified in seconds.

        Return a tuple of (new_grid, update_time).
        """
        logger.info("Updating pattern")

        # Initialise an all-off silent grid
        grid = np.zeros((7, 7, 6), dtype=np.uint8)

        if self.config is not None:
            # If given a config, set the whole grid to that colour
            grid[:, :, :3] = self.config["colour"]
        else:
            # Otherwise set the whole grid green
            grid[:, :, 1] = 255

        # Run again in 1/30 of a second, ie 30fps
        return grid, 1/30
