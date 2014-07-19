import pyglet
import numpy as np

from .timeline import Timeline


class AudioTimeline(Timeline):
    w = 502
    h = 256

    start_time = 0.0
    current_time = 0.0
    end_time = 1.0

    beats = False

    def __init__(self, *args, **kwargs):
        super(AudioTimeline, self).__init__(*args, **kwargs)
        self.time_verts = pyglet.graphics.vertex_list(0, ('v2f', []))
        self.beat_verts = pyglet.graphics.vertex_list(0, ('v2f', []))
        self.amp_verts = pyglet.graphics.vertex_list(0, ('v2f', []))
        if 'audio' in kwargs:
            self.set_audio(kwargs['audio'])
        if 'start' in kwargs and 'end' in kwargs:
            self.set_times(kwargs['start'], kwargs['end'])
        if 'time' in kwargs:
            self.set_time(kwargs['time'])

        audio = pyglet.media.load("/home/adam/Music/Anamanaguchi/PopIt.wav",
                                  streaming=False)
        self.set_audio(audio)
        self.set_times(0.0, 5.0)
        self.set_time(1.7)
        self.set_beats([1.0, 1.5, 2.0, 2.5])

    def set_audio(self, audio):
        self.audio = audio
        data = np.fromstring(audio._data, dtype=np.int16).reshape((-1, 2))
        self.data = data.astype(np.float).sum(axis=1) / 65536.0
        self.sr = audio.audio_format.sample_rate
        self.current_time = 0.0
        self.resize()

    def set_times(self, start, end):
        self.start_time = start
        self.end_time = end
        self.resize()

    def set_time(self, time):
        self.current_time = time
        self.compute_time_line()

    def set_beats(self, beats):
        self.beats = beats

    def compute_audio_amplitudes(self):
        duration = self.end_time - self.start_time
        skip = int((self.sr * duration) / self.w)
        n = skip * self.w
        start = self.sr * self.start_time
        data = self.data[start:start+n].reshape((-1, skip))
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
        del self.amp_verts
        self.amp_verts = pyglet.graphics.vertex_list(
            len(verts)//2, ('v2f\static', verts), ('c3B\static', colours))

    def compute_time_line(self):
        duration = self.end_time - self.start_time
        progress = (self.current_time + self.start_time) / duration
        x = self.x + progress * self.w
        y1 = self.y
        y2 = y1 + self.h
        del self.time_verts
        self.time_verts = pyglet.graphics.vertex_list(
            2, ('v2f\dynamic', [x, y1, x, y2]), ('c3B\static', [0, 255, 0]*2))

    def compute_beat_lines(self):
        if not self.beats:
            return
        start, end = self.beats[0], self.beats[-1]
        self.beat_spacing = (end - start) / len(self.beats)
        self.first_beat = start % self.beat_spacing
        first_beat = self.start_time + self.start_time % self.beat_spacing
        b = np.arange(first_beat, self.end_time, self.beat_spacing)
        p = (b + self.start_time) / (self.end_time - self.start_time)
        x = self.x + p * self.w
        y1 = np.repeat((self.y,), x.size)
        y2 = y1 + self.h
        colours = np.tile(np.array((255, 0, 255), dtype=np.uint8), x.size * 2)
        verts = np.vstack((x, y1, x, y2)).T.reshape((-1))
        del self.beat_verts
        self.beat_verts = pyglet.graphics.vertex_list(
            len(verts)//2, ('v2f\static', verts), ('c3B\static', colours))

    def resize(self):
        self.compute_audio_amplitudes()
        self.compute_beat_lines()
        self.compute_time_line()

    def draw(self):
        self.amp_verts.draw(pyglet.gl.GL_LINES)
        self.beat_verts.draw(pyglet.gl.GL_LINES)
        self.time_verts.draw(pyglet.gl.GL_LINES)
