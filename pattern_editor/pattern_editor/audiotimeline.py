import pyglet
import numpy as np

from .timeline import Timeline


class AudioTimeline(Timeline):
    """
    A timeline that shows a section of the current song by its amplitude,
    and allows for clicking to place beat markers.
    """
    audio = None
    beats = []

    def __init__(self, *args, audiofile=None, **kwargs):
        super(AudioTimeline, self).__init__(*args, **kwargs)
        self.beat_verts = pyglet.graphics.vertex_list(0, 'v2f')
        self.amp_verts = pyglet.graphics.vertex_list(0, 'v2f')
        if audiofile:
            self.load_audio(audiofile)

    def load_audio(self, audiofile):
        self.audio = pyglet.media.load(audiofile, streaming=False)
        self.player = pyglet.media.Player()
        self.player.queue(self.audio)
        self.player.eos_action = self.player.EOS_LOOP
        data = np.fromstring(self.audio._data, dtype=np.int16).reshape((-1, 2))
        self.data = data.astype(np.float).sum(axis=1) / 65536.0
        self.sr = self.audio.audio_format.sample_rate
        self.current_time = 0.0
        self.resize()

    def playpause(self):
        if self.player.playing:
            self.player.pause()
        else:
            self.player.play()

    def compute_audio_amplitudes(self):
        if not self.audio:
            self.amp_verts.delete()
            self.amp_verts = pyglet.graphics.vertex_list(0, 'v2f')
            return

        duration = self.end_time - self.start_time
        condense = int((self.sr * duration) / self.w)
        n = condense * self.w
        start = int(self.sr * self.start_time)
        data = self.data[start:start+n].reshape((-1, condense))
        x = np.linspace(self.x, self.w, data.shape[0])
        pks = abs(data).max(axis=1)
        rms = np.sqrt(np.mean(data**2, axis=1))
        y_pk_p = self.y + self.h/2 + self.h/2 * pks
        y_pk_n = self.y + self.h/2 + self.h/2 * -pks
        y_rms_p = self.y + self.h/2 + self.h/2 * rms
        y_rms_n = self.y + self.h/2 + self.h/2 * -rms
        verts_pk = np.vstack((x, y_pk_p, x, y_pk_n)).T.reshape((-1))
        verts_rms = np.vstack((x, y_rms_p, x, y_rms_n)).T.reshape((-1))
        vn = verts_pk.size // 2
        colours_pk = np.tile(np.array((100, 100, 100), dtype=np.uint8), vn)
        colours_rms = np.tile(np.array((255, 255, 255), dtype=np.uint8), vn)
        verts = np.hstack((verts_pk, verts_rms))
        colours = np.hstack((colours_pk, colours_rms))
        self.amp_verts.delete()
        self.amp_verts = pyglet.graphics.vertex_list(
            len(verts)//2, ('v2f\static', verts), ('c3B\static', colours))

    def compute_beat_lines(self):
        if len(self.beats) == 0:
            self.beat_verts.delete()
            self.beat_verts = pyglet.graphics.vertex_list(0, ('v2f', []))
            return

        if len(self.beats) == 1:
            d = self.end_time - self.start_time
            p = (self.beats[0] - self.start_time) / d
            x = self.x + p * self.w
            y1 = float(self.y)
            y2 = float(y1 + self.h)
            c = [255, 0, 255, 255, 0, 255]
            v = [x, y1, x, y2]
            self.beat_verts.delete()
            self.beat_verts = pyglet.graphics.vertex_list(
                len(v)//2, ('v2f\static', v), ('c3B\static', c))
            return

        start, end = self.beats[0], self.beats[-1]
        self.beat_spacing = (end - start) / (len(self.beats) - 1)
        self.first_beat = start % self.beat_spacing

        t0 = self.first_beat
        t = self.start_time
        d = self.beat_spacing

        first_beat = (((t - t0)//d) + 1) * d + t0

        b = np.arange(first_beat, self.end_time, self.beat_spacing)
        p = (b - self.start_time) / (self.end_time - self.start_time)
        x = self.x + p * self.w
        y1 = np.repeat((self.y,), x.size)
        y2 = y1 + self.h
        colours = np.tile(np.array((255, 0, 255), dtype=np.uint8), x.size * 2)
        verts = np.vstack((x, y1, x, y2)).T.reshape((-1))
        self.beat_verts.delete()
        self.beat_verts = pyglet.graphics.vertex_list(
            len(verts)//2, ('v2f\static', verts), ('c3B\static', colours))

    def next_beat_time(self):
        if len(self.beats) in (0, 1):
            return self.current_time

        t = self.current_time + 0.001
        t0 = self.first_beat
        d = self.beat_spacing

        return min(self.audio.duration, (((t - t0)//d) + 1) * d + t0)

    def prev_beat_time(self):
        if len(self.beats) in (0, 1):
            return self.current_time

        t = self.current_time - 0.001
        t0 = self.first_beat
        d = self.beat_spacing

        return max(0.0, ((t - t0)//d) * d + t0)

    def resize(self):
        super(AudioTimeline, self).resize()
        self.compute_audio_amplitudes()
        self.compute_beat_lines()

    def draw(self):
        self.amp_verts.draw(pyglet.gl.GL_LINES)
        self.beat_verts.draw(pyglet.gl.GL_LINES)
        super(AudioTimeline, self).draw()

    def mousepress(self, x, y, btn, mod):
        super(AudioTimeline, self).mousepress(x, y, btn, mod)
        if mod & pyglet.window.key.MOD_SHIFT:
            if btn == pyglet.window.mouse.RIGHT:
                self.beats = []
                self.compute_beat_lines()
            if btn == pyglet.window.mouse.LEFT:
                t = (x / self.w) * (self.end_time - self.start_time)
                self.beats.append(self.start_time + t)
                self.compute_beat_lines()
