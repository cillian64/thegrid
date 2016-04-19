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
from colorsys import hsv_to_rgb

@register_pattern("Gridi")
class Sample(Pattern):
    def __init__(self, cfg, tracking):
        logger.info("Starting Gridi")
        self.gen = self.generator()
        self.midi_p = midi.read_midifile("thegrid/patterns/polka.mid")
        self.midi_res = self.midi_p.resolution
        self.midi_t = self.midi_p[np.argmax([len(t) for t in self.midi_p])]
        self.t_delay = 60 / 120 / self.midi_res
        self.state = np.zeros((7, 7, 3), dtype=np.int)

    def generator(self):
        for event in self.midi_t:
            if event.tick != 0:
                yield self.state, self.t_delay*event.tick

            if isinstance(event, midi.SetTempoEvent):
                tempo = event.get_bpm()
                self.t_delay = 60 / tempo / self.midi_res

            if isinstance(event, midi.NoteOnEvent):
                v = event.velocity / 127.0
                hue = (event.pitch % 12) / 12.0
                rgbf = hsv_to_rgb(hue, 1.0, v)
                rgb = tuple(int(x*255) for x in rgbf)
                if event.channel <= 5:
                    self.state[0, event.channel] = rgb
                else:
                    self.state[1, event.channel - 6] = rgb

    def update(self):
        return next(self.gen)
