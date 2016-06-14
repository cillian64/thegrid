"""
The patterns package contains all the pattern modules, plus a decorator and
base class in `patterns.pattern`.

Add any new patterns here with `from . import <name>`.
"""

from . import pong, amaze, sparkle, playlist, static_patterns, on, sample
from . import pattern_one, strike, lightning
from . import snake, diffusion, colourwheel, radar
from .musicpatterns import thegrid
try:
    import cv2
except:
    pass
else:
    from . import simplecv

from .pattern import loaded_patterns

