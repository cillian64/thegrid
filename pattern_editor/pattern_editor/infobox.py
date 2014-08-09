import pyglet

from .control import Control


STATUS_TEXT = """
Time: {ctime:.3f}/{ttime:.3f}
File: {patternf}
Audio: {audiof}
"""

HELP_TEXT = """
SPACE  Play/pause       ]     Zoom In      SHIFT+LMB Audio     Place beat marks
B      All On           [     Zoom Out     SHIFT+RMB Audio     Clear beat marks
b      All Off          n     Prev Beat    LMB(+Drag) Grid     Turn on pole
INS/A  Create Frame     m     Next Beat    RMB(+Drag) Grid     Turn off pole
DEL/D  Delete Frame     ,     Prev Frame   LMB Timeline        Jump to time
s      Save             .     Next Frame
"""


class InfoBox(Control):
    """Display status and help text."""
    h = 256
    w = 512
    ctime = 0.0

    def __init__(self, *args, **kwargs):
        super(InfoBox, self).__init__(*args, **kwargs)
        self.status_text = pyglet.text.Label(
            STATUS_TEXT, font_name="Ubuntu", font_size=10,
            width=self.w, multiline=True, anchor_y='bottom')
        self.help_text = pyglet.text.Label(
            HELP_TEXT, font_name="Ubuntu Mono", font_size=8,
            width=self.w, multiline=True, anchor_y='bottom')
        self.ttime = self.parent.audioline.audio.duration
        self.patternf = self.parent.main.patternfile
        self.audiof = self.parent.main.audiofile

    def set_time(self, t):
        self.ctime = t

    def draw(self):
        self.help_text.x = self.x
        self.help_text.y = self.y
        self.help_text.width = self.w
        self.help_text.height = int(0.7 * self.h)
        self.help_text.draw()

        self.status_text.text = STATUS_TEXT.format(
            patternf=self.patternf, audiof=self.audiof,
            ctime=self.ctime, ttime=self.ttime)
        self.status_text.x = self.x
        self.status_text.y = self.y + self.help_text.height
        self.status_text.width = self.w
        self.status_text.height = int(0.3 * self.h)
        self.status_text.draw()
