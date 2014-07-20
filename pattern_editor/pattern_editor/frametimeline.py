import pyglet
import bisect
import numpy as np

from .timeline import Timeline


class FrameTimeline(Timeline):
    """
    A timeline that shows where frames are, time tickers, and allows clicking
    to jump to frames or in time.
    """
    frames = []
    tick_labels = []

    def __init__(self, *args, **kwargs):
        super(FrameTimeline, self).__init__(*args, **kwargs)
        self.tick_verts = pyglet.graphics.vertex_list(0, ('v2f', []))
        self.frame_verts = pyglet.graphics.vertex_list(0, ('v2f', []))
        self.tick_batch = pyglet.graphics.Batch()

    def compute_frame_lines(self):
        duration = self.end_time - self.start_time
        p = (np.array(self.frames) - self.start_time) / duration
        x = self.x + p * self.w
        y1 = np.repeat((self.y,), x.size)
        y2 = y1 + self.h
        verts = np.vstack((x, y1, x, y2)).T.reshape((-1))
        colours = np.tile(np.array((0, 255, 255), dtype=np.uint8), x.size * 2)
        self.frame_verts.delete()
        self.frame_verts = pyglet.graphics.vertex_list(
            x.size*2, ('v2f\static', verts), ('c3B\static', colours))

    def compute_time_texts(self):
        n_ticks = self.w // 50
        duration = self.end_time - self.start_time
        tick0 = self.start_time + duration/20
        tickn = self.end_time - duration/20
        tickspan = (tickn - tick0) / (n_ticks - 1)
        ticks = np.arange(tick0, tickn, tickspan)
        x = self.x + self.w * ((ticks - self.start_time)/duration)
        y1 = np.repeat((self.y + self.h,), x.size)
        y2 = y1 - 10
        verts = np.vstack((x, y1, x, y2)).T.reshape((-1))
        self.tick_verts.delete()
        self.tick_verts = pyglet.graphics.vertex_list(
            x.size*2, ('v2f\static', verts))
        del self.tick_labels[:]
        self.tick_batch = pyglet.graphics.Batch()
        for tick_x, tick_t in zip(x, ticks):
            label = pyglet.text.Label(
                "{:.2f}".format(tick_t), font_name='Ubuntu Mono',
                font_size=10, x=tick_x, y=(self.y+self.h-10),
                anchor_x='center', anchor_y='top', batch=self.tick_batch)
            self.tick_labels.append(label)

    def resize(self):
        super(FrameTimeline, self).resize()
        self.compute_frame_lines()
        self.compute_time_texts()

    def draw(self):
        self.frame_verts.draw(pyglet.gl.GL_LINES)
        self.tick_verts.draw(pyglet.gl.GL_LINES)
        self.tick_batch.draw()
        super(FrameTimeline, self).draw()

    def add_frame(self):
        bisect.insort(self.frames, self.current_time)
        self.compute_frame_lines()

    def remove_frame(self):
        ft = bisect.bisect(self.frames, self.current_time)
        if 0 < ft <= len(self.frames):
            del self.frames[ft - 1]
            self.compute_frame_lines()
