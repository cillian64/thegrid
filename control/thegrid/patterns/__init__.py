"""
The patterns package contains all the pattern modules, plus a decorator and
base class in `patterns.pattern`.

Add any new patterns here with `from . import <name>`.
"""

from . import pong
from . import amaze
from . import sparkle
from . import playlist
from . import static_patterns
from . import on
from . import sample
from . import pattern_one
from . import strike
from . import lightning
from . import fire
from . import spotlights
from . import snake
from . import diffusion
from . import colourwheel
from . import radar
from . import colourwave
from . import grid_of_life

# The other imports have optional dependencies:
try: import cv2
except: pass
else: from . import simplecv

try: import alsaaudio
except: pass
else: from . import vu, spectrogram

try: import midi.sequencer
except: pass
else: from . import gridi

try: import pyglet
except: pass
else: from .musicpatterns import thegrid, captainkirk

from .pattern import loaded_patterns

