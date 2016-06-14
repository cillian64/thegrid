"""
gridi.py

MIDI playback pattern
"""

import logging
import numpy as np
from .pattern import Pattern, register_pattern
logger = logging.getLogger(__name__)

import time
import midi
import midi.sequencer
from colorsys import hsv_to_rgb
import time

@register_pattern("Gridi")
class Sample(Pattern):
    def __init__(self, cfg, tracking):
        logger.info("Starting Gridi")
        self.gen = self.generator()
        self.midi_p = midi.read_midifile("thegrid/patterns/canyon.mid")
        self.midi_res = self.midi_p.resolution
        self.midi_p.make_ticks_abs()
        self.events = self.midi_p[np.argmax([len(t) for t in self.midi_p])]
        self.events = []
        for t in self.midi_p:
            for event in t:
                self.events.append(event)
        self.events.sort(key=lambda x: x.tick)
        self.t_delay = 60 / 120 / self.midi_res
        self.state = np.zeros((7, 7, 3), dtype=np.uint8)

        self.midi_client = 128
        self.midi_port = 0
        self.hw = midi.sequencer.SequencerHardware()
        self.seq = midi.sequencer.SequencerWrite(
                sequencer_resolution=self.midi_res)
        self.seq.subscribe_port(self.midi_client, self.midi_port)
        self.seq.start_sequencer()

        self.channels = []
        for event in self.events:
            if isinstance(event, midi.NoteOnEvent):
                if event.channel not in self.channels:
                    self.channels.append(event.channel)

        self.poles_per_ch = 49 // len(self.channels)
        self.channels.sort()

    def generator(self):
        t0 = time.time()
        for event in self.events:
            current_ticks = (time.time() - t0) / self.t_delay
            if event.tick - current_ticks > 0:
                yield self.state, self.t_delay*(event.tick - current_ticks)
            self.seq.event_write(event, False, False, True)

            if isinstance(event, midi.SetTempoEvent):
                tempo = event.get_bpm()
                self.t_delay = 60 / tempo / self.midi_res

            if isinstance(event, midi.NoteOnEvent):
                v = event.velocity / 127.0
                hue = (event.pitch % 12) / 12.0
                rgbf = hsv_to_rgb(hue, 1.0, v)
                rgb = tuple(int(x*255) for x in rgbf)
                firstpole = (self.channels.index(event.channel) *
                             self.poles_per_ch)
                self.state.reshape(49, 3)[firstpole:
                        firstpole+self.poles_per_ch] = rgb

            if isinstance(event, midi.NoteOffEvent):
                firstpole = (self.channels.index(event.channel) *
                             self.poles_per_ch)
                self.state.reshape(49, 3)[firstpole:
                        firstpole+self.poles_per_ch] = (0, 0, 0)

    def update(self):
        return next(self.gen)
