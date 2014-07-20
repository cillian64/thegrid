import pyglet

from .audiotimeline import AudioTimeline
from .frametimeline import FrameTimeline
from .griddisplay import GridDisplay
from .infobox import InfoBox


class EditorWindow(pyglet.window.Window):
    w = 512
    h = 1024
    padding = 5

    def __init__(self, *args, main, audiofile, **kwargs):
        self.main = main
        self.audioline = AudioTimeline(
            self, *args, audiofile=audiofile, **kwargs)
        self.frameline = FrameTimeline(self, *args, **kwargs)
        self.griddisplay = GridDisplay(self, *args, **kwargs)
        ttime = self.audioline.audio.duration
        self.infobox = InfoBox(self, *args, ttime=ttime, **kwargs)

        self.controls = [
            self.audioline, self.frameline, self.griddisplay, self.infobox]

        super(EditorWindow, self).__init__(
            caption='Pattern Editor', visible=True, resizable=True,
            width=512, height=768)

    def on_resize(self, width, height):
        super(EditorWindow, self).on_resize(width, height)

        self.audioline.w = width - self.padding
        self.frameline.w = width - self.padding
        self.infobox.w = width - self.padding * 2

        self.audioline.h = int(height * 0.125)
        self.frameline.h = int(height * 0.125)
        self.infobox.h = int(height * 0.25)

        grid_h, grid_w = height//2, width - 2*self.padding
        grid_s = min(grid_h, grid_w)
        self.griddisplay.w = self.griddisplay.h = grid_s

        self.audioline.x = self.padding
        self.frameline.x = self.padding
        self.infobox.x = self.padding
        self.griddisplay.x = self.padding
        if (width - 2*self.padding) > grid_s:
            self.griddisplay.x += (width - grid_s - 2*self.padding)//2

        self.infobox.y = 0
        self.griddisplay.y = self.infobox.h
        if height//2 > grid_s:
            self.griddisplay.y += (height//2 - grid_s)//2
        self.frameline.y = self.griddisplay.y + self.griddisplay.h
        self.audioline.y = self.frameline.y + self.frameline.h

        for control in self.controls:
            control.resize()

    def on_draw(self):
        self.clear()
        for control in self.controls:
            control.draw()

    def on_key_press(self, sym, mod):
        self.main.handle_keypress(sym, mod)

    def on_mouse_press(self, x, y, btn, mod):
        for control in self.controls:
            control.check_mousepress(x, y, btn, mod)

    def on_mouse_drag(self, x, y, dx, dy, btns, mod):
        for control in self.controls:
            control.check_mousedrag(x, y, dx, dy, btns, mod)
