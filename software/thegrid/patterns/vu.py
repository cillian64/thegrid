import alsaaudio

import numpy as np
from scipy.signal import lfilter, firwin

from ..pattern import Pattern, register_pattern, clicker



red = (255, 0, 0)
orange = (255, 80, 0)
green = (0, 255, 0)
off = (0, 0, 0)

@register_pattern("VU")
@clicker()
class PatternVU(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator()

    def generator(self):
        gain = 0.3
        agc_setpoint = 10000.0
        agc_rate = 0.005
        agc_min = 0.0
        agc_max = 10.0
        block_size = 1024
        sampling_rate = 44100
        filter_n = 512
        filter_h = firwin(filter_n, 10.0, nyq=sampling_rate / 2)
        zi = np.zeros(filter_n - 1)
        pcm = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE)
        pcm.setperiodsize(block_size)
        pcm.setrate(sampling_rate)
        samples = np.empty(block_size * 100)
        envelope = np.empty(block_size * 100)
        lenvs = np.empty(block_size * 100)
        lights = np.zeros((7, 7, 3), dtype=np.uint8)
        while True:
            n_frames, frames = pcm.read()
            n_frames, frames = pcm.read()
            n_frames, frames = pcm.read()
            frames = np.fromstring(frames, dtype='<i2').reshape((-1, 2))
            rectified = gain * np.abs(frames[:, 0] + frames[:, 1])

            agc_error = agc_setpoint - np.max(rectified)
            if agc_error > 0:
                gain += agc_rate
            else:
                gain -= agc_rate
            gain = gain if agc_min <= gain <= agc_max else (
                agc_min if gain < 0 else agc_max)

            env, zi = lfilter(filter_h, 1.0, rectified, zi=zi)
            lenv = env
            #lenvs[i*block_size:(i+1)*block_size] = lenv
            #level = int((np.max(lenv) - 2000)/1000)
            level = int(np.max(env) / 1000)
            level = level if 0 <= level <= 6 else (0 if level < 0 else 6)
#            print(["#"]*level)

            colours = [
                (0, 255, 0),
                (0, 255, 0),
                (0, 255, 0),
                (255, 80, 0),
                (255, 80, 0),
                (255, 0, 0),
                (255, 0, 0)]

            for i in range(7):
                if i <= level:
                    lights[6-i, :] = colours[i]
                else:
                    lights[6-i, :] = (0, 0, 0)

            yield lights, 0.001

    def update(self):
        return self.gen.__next__()

