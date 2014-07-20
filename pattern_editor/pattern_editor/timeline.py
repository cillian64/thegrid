import pyglet

from .control import Control


class Timeline(Control):
    """Base Timeline class for AudioTimeline and FrameTimeline"""
    h = 128
    w = 512
    start_time = 0.0
    current_time = 0.0
    end_time = 4.0

    def __init__(self, *args, **kwargs):
        super(Timeline, self).__init__(*args, **kwargs)
        self.time_verts = pyglet.graphics.vertex_list(0, ('v2f', []))
        if 'start' in kwargs and 'end' in kwargs:
            self.set_times(kwargs['start'], kwargs['end'])
        if 'time' in kwargs:
            self.set_time(kwargs['time'])

    def set_times(self, start, end):
        self.start_time = start
        self.end_time = end
        self.resize()

    def set_time(self, time):
        self.current_time = time
        self.compute_time_line()

    def compute_time_line(self):
        duration = self.end_time - self.start_time
        progress = (self.current_time - self.start_time) / duration
        x = self.x + progress * self.w
        y1 = self.y
        y2 = y1 + self.h
        self.time_verts.delete()
        self.time_verts = pyglet.graphics.vertex_list(
            2, ('v2f\dynamic', [x, y1, x, y2]), ('c3B\static', [0, 255, 0]*2))

    def resize(self):
        self.compute_time_line()

    def draw(self):
        self.time_verts.draw(pyglet.gl.GL_LINES)

    def mousepress(self, x, y, btn, mod):
        if btn == pyglet.window.mouse.LEFT:
            if mod & pyglet.window.key.MOD_SHIFT:
                return
            t = (x / self.w) * (self.end_time - self.start_time)
            t += self.start_time
            self.parent.main.set_time(t)
            self.parent.audioline.player.seek(t)

    def mousedrag(self, x, y, dx, dy, btns, mod):
        if btns & pyglet.window.mouse.LEFT:
            if mod & pyglet.window.key.MOD_SHIFT:
                return
            if self.parent.audioline.player.playing:
                return
            t = (x / self.w) * (self.end_time - self.start_time)
            t += self.start_time
            self.parent.main.set_time(t)
            self.parent.audioline.player.seek(t)
