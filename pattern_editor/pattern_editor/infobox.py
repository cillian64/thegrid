import pyglet

from .control import Control


STATUS_TEXT = """
File: {patternf}
Audio: {audiof}
Time: {ctime:.3f}/{ttime:.3f}
"""

HELP_TEXT = """
Space: Play/pause
d: Delete Frame
d: Delete Frame
d: Delete Frame
d: Delete Frame
d: Delete Frame
"""


class InfoBox(Control):
    h = 256
    w = 512

    def __init__(self, *args, **kwargs):
        super(InfoBox, self).__init__(*args, **kwargs)
        self.status_text = pyglet.text.Label(
            STATUS_TEXT, font_name="Ubuntu", font_size=10,
            width=350, multiline=True)
        self.help_text = pyglet.text.Label(
            HELP_TEXT, font_name="Ubuntu", font_size=10,
            width=162, multiline=True, align="right")

    def draw(self):
        self.status_text.text = STATUS_TEXT.format(
            patternf="/tmp/whatev", audiof="~/nope.mp3",
            ctime=0, ttime=123.45)
        self.status_text.x = self.x
        self.status_text.y = self.y
        self.status_text.width = int(0.7 * self.w)
        self.status_text.height = self.h
        self.status_text.draw()

        self.help_text.x = self.x + self.status_text.width
        self.help_text.y = self.y
        self.help_text.width = int(0.3 * self.w)
        self.help_text.height = self.h
        self.help_text.draw()
