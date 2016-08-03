"""
List all patterns to load here.
You can add logic around the import statement to check for dependencies etc.
"""
# Import the full list of loaded patterns
from ..pattern import loaded_patterns

# Import all patterns to load below here
from . import pong
from . import sparkle
from . import playlist
from . import static_patterns
from . import on
from . import sample
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
from . import colour_ripple
from . import stopping
from . import soundtest

# The other imports have optional dependencies:
try: import alsaaudio
except: pass
else: from . import vu, spectrogram

try: import midi.sequencer
except: pass
else: from . import gridi

try: import pyglet
except: pass
else: from .musicpatterns import captainkirk
