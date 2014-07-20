import pyglet
from .editorwindow import EditorWindow


class Main:
    zoom = 4.0
    start_time = 0.0
    current_time = 0.0
    end_time = 4.0

    def __init__(self, patternfile, audiofile):
        self.patternfile = patternfile
        self.audiofile = audiofile
        self.window = EditorWindow(
            main=self, audiofile=audiofile)

    def run(self):
        pyglet.clock.schedule_interval(self.tick, 1/50)
        pyglet.app.run()

    def handle_keypress(self, sym, mod):
        if sym == pyglet.window.key.SPACE:
            self.window.audioline.playpause()
        elif sym == pyglet.window.key.BRACKETRIGHT:
            self.update_zoom(0.5)
        elif sym == pyglet.window.key.BRACKETLEFT:
            self.update_zoom(2.0)
        elif sym == pyglet.window.key.B:
            self.window.griddisplay.blanking(mod)
        elif sym == pyglet.window.key.INSERT:
            self.add_frame()
        elif sym == pyglet.window.key.DELETE:
            self.remove_frame()
        elif sym == pyglet.window.key.LEFT:
            self.prev_time_block()
        elif sym == pyglet.window.key.RIGHT:
            self.next_time_block()
        elif sym == pyglet.window.key.S:
            self.save()
        elif sym == pyglet.window.key.N:
            self.prev_beat()
        elif sym == pyglet.window.key.M:
            self.next_beat()
        elif sym == pyglet.window.key.COMMA:
            self.prev_frame()
        elif sym == pyglet.window.key.PERIOD:
            self.next_frame()

    def update_zoom(self, factor):
        if self.zoom * factor < 0.125 or self.zoom * factor > 1000.0:
            return

        self.zoom *= factor
        center = self.current_time

        self.start_time = center - self.zoom
        if self.start_time < 0.0:
            self.start_time = 0.0

        self.end_time = self.start_time + self.zoom
        if self.end_time > self.window.audioline.audio.duration:
            self.end_time = self.window.audioline.audio.duration

        for control in self.window.controls:
            control.set_times(self.start_time, self.end_time)

    def tick(self, dt):
        t = self.window.audioline.player.time
        self.current_time = t
        for control in self.window.controls:
            control.set_time(t)
        if t > self.end_time:
            self.next_time_block()

    def set_time(self, t):
        self.current_time = t
        for control in self.window.controls:
            control.set_time(t)

    def seek_time(self, t):
        self.window.audioline.player.seek(t)
        self.set_time(t)

    def next_time_block(self):
        overlap = self.zoom * 0.1
        self.start_time = self.end_time - overlap
        self.end_time = self.start_time + self.zoom
        if self.end_time > self.window.audioline.audio.duration:
            self.end_time = self.window.audioline.audio.duration
        for control in self.window.controls:
            control.set_times(self.start_time, self.end_time)

    def prev_time_block(self):
        overlap = self.zoom * 0.1
        self.end_time = self.start_time + overlap
        self.start_time = self.end_time - self.zoom
        if self.start_time < 0.0:
            self.start_time = 0.0
        for control in self.window.controls:
            control.set_times(self.start_time, self.end_time)

    def add_frame(self):
        self.window.frameline.add_frame()

    def remove_frame(self):
        self.window.frameline.remove_frame()

    def prev_frame(self):
        pass

    def next_frame(self):
        pass

    def prev_beat(self):
        self.seek_time(self.window.audioline.prev_beat_time())

    def next_beat(self):
        self.seek_time(self.window.audioline.next_beat_time())

    def save(self):
        pass
