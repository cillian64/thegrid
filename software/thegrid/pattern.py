import numpy as np
import logging
logger = logging.getLogger(__name__)

loaded_patterns = {}


def register_pattern(name, config=None):
    def wrapper(pattern):
        loaded_patterns[name] = (pattern, config)
        logger.info("Registered pattern %s", name)
        return pattern
    return wrapper


def monochrome(colour=None):
    """
    Turn a monochrome pattern (which returns only (7, 7) shaped bool results)
    into a colour pattern of a specified colour (silent white by default).

    Specify a 3-long tuple (RGB only) or a 6-long tuple (sound included) for
    colour, such as (255, 0, 255) or (255, 0, 255, 1, 200, 255).
    """
    if colour is None:
        colour = (255, 255, 255)
    colour = np.array(colour).reshape(1, -1)
    if colour.size == 3:
        colour = np.append(colour, (0, 0, 0)).reshape(1, -1)
    assert colour.shape == (1, 6)

    def wrapper(pattern):
        class NewPattern(pattern):

            def update(self):
                poles, delay = super().update()
                return poles.reshape(7, 7, 1).dot(colour), delay
        NewPattern.__name__ = "{}_monochrome".format(pattern.__name__)
        return NewPattern
    return wrapper


def clicker(freq=255, vol=255):
    """
    Replace the sound from a pattern with a click whenever a pole changes
    colour from one frame to the next.
    Optionally specify the frequency and volume to use.
    """
    def wrapper(pattern):
        class NewPattern(pattern):
            last_poles = np.zeros((7, 7, 3), dtype=np.uint8)

            def update(self):
                poles, delay = super().update()
                new_poles = poles.copy().reshape(7, 7, -1)[:, :, :3]
                changed = np.any(new_poles != self.last_poles, axis=2)
                sound = np.array((5, freq, vol), dtype=np.uint8).reshape(1, 3)
                sounds = changed.reshape(7, 7, 1).dot(sound)
                poles = np.concatenate((new_poles, sounds), axis=2)
                self.last_poles = new_poles
                return poles, delay
        NewPattern.__name__ = "{}_clicker".format(pattern.__name__)
        return NewPattern
    return wrapper


class Pattern:
    def __init__(self, config, ui):
        self.config = config
        self.ui = ui

    def update(self):
        raise NotImplementedError
