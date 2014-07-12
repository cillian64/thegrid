"""
pattern.py

The base class and decorator for patterns to inherit from.
"""

import logging
logger = logging.getLogger(__name__)

loaded_patterns = {}


def register_pattern(name, config=None):
    """
    Use this decorator to register a new pattern.
    Name is used for the global name list and config will be passed back
    to the pattern's constructor at runtime.
    You may register the same pattern class multiple times under different
    names (typically with different configs).
    """
    def wrapper(pattern):
        loaded_patterns[name] = (pattern, config)
        logger.info("Registered pattern {}".format(name))
        return pattern
    return wrapper


class Pattern:
    """
    Pattern classes are responsible for updating the grid to some new state,
    based on time, previous states or tracking information.

    They will be created when they start running on the grid, and destroyed
    once a new pattern takes over.
    """

    def __init__(self, config, tracking):
        """
        __init__ will be called with (config, tracking) arguments and you may
        do what you will with them.
        """
        self.config = config
        self.tracking = tracking

    def update(self):
        """
        This function will be called every time control is ready to update the
        grid, on an irregular basis. It should return a tuple of
        (the desired grid state as a 7x7 numpy boolean array,
         the time to display this frame in seconds).
        """
        raise NotImplementedError
