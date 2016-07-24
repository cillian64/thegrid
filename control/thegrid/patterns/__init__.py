"""
The patterns package contains all the pattern modules, plus a decorator and
base class in `patterns.pattern`.

Add any new patterns here with `from . import <name>`.
"""

from . import pong, amaze, sparkle, playlist, static_patterns, on, sample
from . import pattern_one, strike, lightning, fire, spotlights
from . import snake, diffusion, colourwheel, radar, colourwave
from . import grid_of_life
from .musicpatterns import thegrid
try:
    import cv2
except:
    pass
else:
    from . import simplecv
try:
    import alsaaudio
except:
    pass
else:
    from . import vu
try:
    import midi.sequencer
except:
    pass
else:
    from . import gridi

from .pattern import loaded_patterns

