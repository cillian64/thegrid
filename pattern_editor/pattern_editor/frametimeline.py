import pyglet
import numpy as np

from .timeline import Timeline


class FrameTimeline(Timeline):
    h = 128
    current_time = 0.0
    frames = []

    def __init__(self, *args, **kwargs):
        super(FrameTimeline, self).__init__(*args, **kwargs)
        self.time_verts = pyglet.graphics.vertex_list(0, ('v2f', []))
        self.tick_verts = pyglet.graphics.vertex_list(0, ('v2f', []))
        self.frame_verts = pyglet.graphics.vertex_list(0, ('v2f', []))
        self.tick_batch = pyglet.graphics.Batch()

        if 'start' in kwargs and 'end' in kwargs:
            self.set_times(kwargs['start'], kwargs['end'])
        if 'time' in kwargs:
            self.set_time(kwargs['time'])
        self.set_times(0.0, 5.0)
        self.set_time(1.7)
        self.frames = [1.1, 1.8, 4.6]

    def set_times(self, start, end):
        self.start_time = start
        self.end_time = end
        self.resize()

    def set_time(self, time):
        self.current_time = time
        self.compute_time_line()

    def compute_time_line(self):
        duration = self.end_time - self.start_time
        progress = (self.current_time + self.start_time) / duration
        x = self.x + progress * self.w
        y1 = self.y
        y2 = y1 + self.h
        del self.time_verts
        self.time_verts = pyglet.graphics.vertex_list(
            2, ('v2f\dynamic', [x, y1, x, y2]), ('c3B\static', [0, 255, 0]*2))

    def compute_frame_lines(self):
        duration = self.end_time - self.start_time
        p = (np.array(self.frames) + self.start_time) / duration
        x = self.x + p * self.w
        y1 = np.repeat((self.y,), x.size)
        y2 = y1 + self.h
        verts = np.vstack((x, y1, x, y2)).T.reshape((-1))
        colours = np.tile(np.array((0, 255, 255), dtype=np.uint8), x.size * 2)
        del self.frame_verts
        self.frame_verts = pyglet.graphics.vertex_list(
            x.size*2, ('v2f\static', verts), ('c3B\static', colours))

    def compute_time_texts(self):
        n_ticks = self.w // 50
        duration = self.end_time - self.start_time
        tick0 = self.start_time + duration/20
        tickn = self.end_time - duration/20
        tickspan = (tickn - tick0) / (n_ticks - 1)
        ticks = np.arange(tick0, tickn, tickspan)
        x = self.x + self.w * ((ticks + self.start_time)/duration)
        y1 = np.repeat((self.y + self.h,), x.size)
        y2 = y1 - 10
        verts = np.vstack((x, y1, x, y2)).T.reshape((-1))
        del self.tick_verts
        self.tick_verts = pyglet.graphics.vertex_list(
            x.size*2, ('v2f\static', verts))
        del self.tick_batch
        self.tick_batch = pyglet.graphics.Batch()
        for tick_x, tick_t in zip(x, ticks):
            pyglet.text.Label(
                "{:.2f}".format(tick_t), font_name='Ubuntu Mono',
                font_size=10, x=tick_x+2, y=(self.y+self.h-5),
                anchor_x='left', anchor_y='center', batch=self.tick_batch)

    def resize(self):
        self.compute_time_line()
        self.compute_frame_lines()
        self.compute_time_texts()

    def draw(self):
        self.frame_verts.draw(pyglet.gl.GL_LINES)
        self.time_verts.draw(pyglet.gl.GL_LINES)
        self.tick_verts.draw(pyglet.gl.GL_LINES)
        self.tick_batch.draw()
