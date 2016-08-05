"""
gridi.py

MIDI playback pattern
"""

import logging
import numpy as np
from ..pattern import Pattern, register_pattern, silent
logger = logging.getLogger(__name__)

import time
import midi
import midi.sequencer
from colorsys import hsv_to_rgb
import time

@register_pattern("[MUSIC] MIDI player: barbie.mid",
                        "thegrid/patterns/mids/barbie.mid")
@register_pattern("[MUSIC] MIDI player: canyon.mid",
                        "thegrid/patterns/mids/canyon.mid")
@register_pattern("[MUSIC] MIDI player: dancingqueen.mid",
                        "thegrid/patterns/mids/dancingqueen.mid")
@register_pattern("[MUSIC] MIDI player: ff7.mid",
                        "thegrid/patterns/mids/ff7.mid")
@register_pattern("[MUSIC] MIDI player: freebird.mid",
                        "thegrid/patterns/mids/freebird.mid")
@register_pattern("[MUSIC] MIDI player: getlucky.mid",
                        "thegrid/patterns/mids/getlucky.mid")
@register_pattern("[MUSIC] MIDI player: bohemian.mid",
                        "thegrid/patterns/mids/bohemian.mid")
@register_pattern("[MUSIC] MIDI player: sweetchild.mid",
                        "thegrid/patterns/mids/sweetchild.mid")
@register_pattern("[MUSIC] MIDI player: tubthumping.mid",
                        "thegrid/patterns/mids/tubthumping.mid")
@register_pattern("[MUSIC] MIDI player: newlife.mid",
                        "thegrid/patterns/mids/newlife.mid")
@register_pattern("[MUSIC] MIDI player: justcantgetenough.mid",
                        "thegrid/patterns/mids/justcantgetenough.mid")
@silent()
class Gridi(Pattern):
    def __init__(self, cfg, ui):
        # This bit is quite tedious.  I apologise.
        self.segmentation = []
        for _ in range(18):
            self.segmentation.append(np.zeros((7, 7), dtype=np.uint8))

        self.segmentation[1][:, :] = 1
        
        self.segmentation[2][:, :] = 2
        self.segmentation[2][0:3, :] = 1
        self.segmentation[2][3, 0:3] = 1

        self.segmentation[3][:, :] = 1
        self.segmentation[3][2, 2:] = 2
        self.segmentation[3][3:5, :] = 2
        self.segmentation[3][4, 5:] = 3
        self.segmentation[3][5:, :] = 3

        self.segmentation[4][:, :] = 1
        self.segmentation[4][:4, 4:] = 2
        self.segmentation[4][4:, 3:] = 3
        self.segmentation[4][3:, :3] = 4

        self.segmentation[5][:, :] = 5
        self.segmentation[5][:3, :3] = 1
        self.segmentation[5][:3, 4:] = 3
        self.segmentation[5][4:, :3] = 2
        self.segmentation[5][4:, 4:] = 4

        self.segmentation[6][:, :] = 1
        self.segmentation[6][:4, 2:4] = 2
        self.segmentation[6][:4, 4:6] = 3
        self.segmentation[6][4:, :3] = 4
        self.segmentation[6][4:, 3:6] = 5

        self.segmentation[7][0, :] = 1
        self.segmentation[7][1, :] = 2
        self.segmentation[7][2, :] = 3
        self.segmentation[7][3, :] = 4
        self.segmentation[7][4, :] = 5
        self.segmentation[7][5, :] = 6
        self.segmentation[7][6, :] = 7

        self.segmentation[8][:, :] = 7
        self.segmentation[8][:, 6] = 8
        self.segmentation[8][:3, :2] = 1
        self.segmentation[8][:3, 2:4] = 2
        self.segmentation[8][:3, 4:6] = 3
        self.segmentation[8][3:6, :2] = 4
        self.segmentation[8][3:6, 2:4] = 5
        self.segmentation[8][3:6, 4:6] = 6

        self.segmentation[9][:, :] = 9
        self.segmentation[9][:2, :2] = 1
        self.segmentation[9][:2, 2:4] = 2
        self.segmentation[9][:2, 4:] = 3
        self.segmentation[9][2:4, :2] = 4
        self.segmentation[9][2:4, 2:4] = 5
        self.segmentation[9][2:4, 4:] = 6
        self.segmentation[9][4:6, :3] = 7
        self.segmentation[9][4:6, 3:] = 8

        self.segmentation[10][:, :] = self.segmentation[9]
        self.segmentation[10][6, 3:] = 10

        self.segmentation[11][:, :] = self.segmentation[9]
        self.segmentation[11][4:6, 5:] = 9
        self.segmentation[11][6, :3] = 10
        self.segmentation[11][6, 3:] = 11

        self.segmentation[12][:, :] = self.segmentation[11]
        self.segmentation[12][:4, 6] = 12

        self.segmentation[13][:, :] = 13
        self.segmentation[13][:3, 0] = 1
        self.segmentation[13][:3, 1] = 2
        self.segmentation[13][:3, 2] = 3
        self.segmentation[13][:3, 3] = 4
        self.segmentation[13][:3, 4] = 5
        self.segmentation[13][:3, 5] = 6
        self.segmentation[13][3:6, 0] = 7
        self.segmentation[13][3:6, 1] = 8
        self.segmentation[13][3:6, 2] = 9
        self.segmentation[13][3:6, 3] = 10
        self.segmentation[13][3:6, 4] = 11
        self.segmentation[13][3:6, 5] = 12

        self.segmentation[14][:, :] = self.segmentation[13]
        self.segmentation[14][6, :] = 14

        self.segmentation[15][:, :] = self.segmentation[14]
        self.segmentation[15][6, 4:] = 15
        self.segmentation[15][4:, 6] = 15

        self.segmentation[16][:, :] = self.segmentation[15]
        self.segmentation[16][6, 3] = 15
        self.segmentation[16][4:, 6] = 16

        # Urgh, that was awful.


        logger.info("Starting Gridi")
        self.gen = self.generator()
        self.midi_p = midi.read_midifile(cfg)
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
        self.channels.sort()

        # Now we know how many channels we have.  We choose the appropriate
        # self.segmentations, then for each channel make a mask array.
        # This part is a little messy becuase the channels may not be
        # sequential, or all exist. e.g. we could just have 1 and 12.
        self.pole_assignments = []
        for idx in range(len(self.channels)):
            self.pole_assignments.append(
                self.segmentation[len(self.channels)] == idx + 1)

    def shutdown(self):
        del self.seq
        del self.hw

    def generator(self):
        t0 = time.time()
        for event in self.events:
            current_ticks = (time.time() - t0) / self.t_delay
            if event.tick - current_ticks > 0:
                yield self.state, self.t_delay*(event.tick - current_ticks)

            # Filter out some event types which timidity finds particularly
            # upsetting.
            if not isinstance(event, (midi.SmpteOffsetEvent, midi.PortEvent,
                    midi.SysexEvent, midi.TimeSignatureEvent,
                    midi.KeySignatureEvent, midi.TrackNameEvent,
                    midi.TextMetaEvent, midi.SequencerSpecificEvent,
                    midi.MarkerEvent, midi.AfterTouchEvent,
                    midi.ChannelPrefixEvent)):
                self.seq.event_write(event, False, False, True)

            if isinstance(event, midi.SetTempoEvent):
                tempo = event.get_bpm()
                self.t_delay = 60 / tempo / self.midi_res

            if isinstance(event, midi.NoteOnEvent):
                v = event.velocity / 127.0
                hue = (event.pitch % 12) / 12.0
                rgbf = hsv_to_rgb(hue, 1.0, v)
                rgb = tuple(int(x*255) for x in rgbf)

                ass_idx = self.channels.index(event.channel)
                mask = self.pole_assignments[ass_idx]
                self.state[mask] = rgb

            if isinstance(event, midi.NoteOffEvent):
                ass_idx = self.channels.index(event.channel)
                mask = self.pole_assignments[ass_idx]
                self.state[mask] = (0, 0, 0)
        
        while True:
            yield np.zeros((7, 7, 3), dtype=np.uint8), 0.5

    def update(self):
        return next(self.gen)
