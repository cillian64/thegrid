import pyglet
import bisect
import numpy as np

from .timeline import Timeline


class FrameTimeline(Timeline):
    """
    A timeline that shows where frames are, time tickers, and allows clicking
    to jump to frames or in time.
    """
    frame_data = {}
    frame_times = []
    tick_labels = []

    def __init__(self, *args, **kwargs):
        super(FrameTimeline, self).__init__(*args, **kwargs)
        self.tick_verts = pyglet.graphics.vertex_list(0, 'v2f')
        self.frame_verts = pyglet.graphics.vertex_list(0, 'v2f')
        self.cframe_verts = pyglet.graphics.vertex_list(0, 'v2f')
        self.tick_batch = pyglet.graphics.Batch()
        self.current_frame = None

    def compute_frame_lines(self):
        duration = self.end_time - self.start_time
        p = (np.array(self.frame_times) - self.start_time) / duration
        x = self.x + p * self.w
        y1 = np.repeat((self.y,), x.size)
        y2 = y1 + self.h
        verts = np.vstack((x, y1, x, y2)).T.reshape((-1))
        colours = np.tile(np.array((0, 255, 255), dtype=np.uint8), x.size * 2)
        self.frame_verts.delete()
        self.frame_verts = pyglet.graphics.vertex_list(
            x.size*2, ('v2f\static', verts), ('c3B\static', colours))

    def compute_current_frame_marker(self):
        if self.current_frame is None:
            self.cframe_verts.delete()
            self.cframe_verts = pyglet.graphics.vertex_list(0, 'v2f')
            return
        duration = self.end_time - self.start_time
        p = (self.frame_times[self.current_frame] - self.start_time) / duration
        x = self.x + p * self.w
        x1 = x - 5
        x2 = x + 5
        y1 = self.y
        y2 = y1 + 15
        verts = (x1, y1, x2, y1, x, y2)
        colours = [0, 255, 255] * 3
        self.cframe_verts.delete()
        self.cframe_verts = pyglet.graphics.vertex_list(
            3, ('v2f\static', verts), ('c3B\static', colours))

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
        self.compute_current_frame_marker()
        self.compute_time_texts()

    def draw(self):
        self.frame_verts.draw(pyglet.gl.GL_LINES)
        self.cframe_verts.draw(pyglet.gl.GL_TRIANGLES)
        self.tick_verts.draw(pyglet.gl.GL_LINES)
        self.tick_batch.draw()
        super(FrameTimeline, self).draw()

    def add_frame(self):
        bisect.insort(self.frame_times, self.current_time)
        state = self.parent.griddisplay.state.copy()
        self.frame_data[self.current_time] = state
        self.compute_frame_lines()
        self.check_frame_change()

    def remove_frame(self):
        ft = self.current_frame_idx()
        if ft is not None and 0 <= ft < len(self.frame_times):
            del self.frame_data[self.frame_times[ft]]
            del self.frame_times[ft]
            self.current_frame = None
            self.compute_frame_lines()
            self.check_frame_change()
            self.compute_current_frame_marker()

    def current_frame_idx(self):
        frame = bisect.bisect(self.frame_times, self.current_time) - 1
        if frame == -1:
            frame = None
        return frame

    def check_frame_change(self):
        new = self.current_frame_idx()
        if new != self.current_frame:
            self.update_current_frame(new)

    def update_current_frame(self, new):
        if self.current_frame is not None:
            old_time = self.frame_times[self.current_frame]
            self.frame_data[old_time] = self.parent.griddisplay.state
        self.current_frame = new
        if self.current_frame is not None:
            new_time = self.frame_times[self.current_frame]
            self.parent.griddisplay.state = self.frame_data[new_time]
        else:
            self.parent.griddisplay.state = np.zeros((7, 7), dtype=np.bool)
        self.parent.griddisplay.compute_lit()
        self.compute_current_frame_marker()

    def set_time(self, time):
        super(FrameTimeline, self).set_time(time)
        self.check_frame_change()

    def prev_frame_time(self):
        if self.current_frame is None or self.current_frame == 0:
            return 0.0
        if self.current_time > self.frame_times[self.current_frame]:
            return self.frame_times[self.current_frame]
        return self.frame_times[self.current_frame - 1]

    def next_frame_time(self):
        if self.current_frame is None:
            if self.frame_times:
                return self.frame_times[0]
            else:
                return 0.0
        if len(self.frame_times) == self.current_frame + 1:
            return self.frame_times[-1]
        return self.frame_times[self.current_frame + 1]
