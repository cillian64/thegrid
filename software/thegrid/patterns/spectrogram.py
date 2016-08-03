import alsaaudio

import numpy as np
from scipy.signal import lfilter, firwin
from scipy.fftpack import fft
import time

from ..pattern import Pattern, register_pattern, clicker



red = (255, 0, 0)
orange = (255, 80, 0)
green = (0, 255, 0)
off = (0, 0, 0)

@register_pattern("Spectrogram")
@clicker()
class PatternVU(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator()

    def generator(self):
        gain = 0.3
        block_size = 128
        sampling_rate = 44100
        fft_size = 16
        pcm = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE,
                            mode=alsaaudio.PCM_NONBLOCK)
        pcm.setperiodsize(block_size)
        pcm.setrate(sampling_rate)
        lights = np.zeros((7, 7, 3), dtype=np.uint8)
        levels = np.zeros((7,))
        ave_min = 0
        ave_max = 200
        
        while True:
            n_frames, frames = pcm.read()
            if n_frames != block_size:
                print("GAH! Buffer underrun")

            # Flush buffer:
            while True:
                n_frames, _ = pcm.read()
                if n_frames == 0:
                    break

            frames = np.fromstring(frames, dtype='<i2').reshape((-1, 2))

            power = np.zeros((int(fft_size/2),))
#            for i in range(int(block_size/fft_size)):
#                lf = fft(frames[i*fft_size:(i+1)*fft_size, 0])
#                rf = fft(frames[i*fft_size:(i+1)*fft_size, 1])
#                f = np.abs(lf) ** 2 + np.abs(rf) ** 2
#                power += f[:int(fft_size/2)]
            lf = fft(frames[:fft_size, 0])
            rf = fft(frames[:fft_size, 1])
            f = np.abs(lf) ** 2 + np.abs(rf) ** 2
            power = f[:int(fft_size/2)]
            power[power < 0] = 0
            power = np.sqrt(np.sqrt(power))
            if ave_min < np.min(power):
                ave_min += 1
            else:
                ave_min -= 1
            power -= ave_min
            if ave_max > np.max(power[1:]) and ave_max > 10:
                ave_max -= 1
            else:
                ave_max += 1
            power *= 5/ave_max
            power[power < 0] = 0
            power[power > 7] = 7

            colours = [(0, 255, 0),
                       (0, 255, 0),
                       (0, 255, 0),
                       (0, 255, 0),
                       (255, 255, 0),
                       (255, 255, 0),
                       (255, 0, 0)]

            for idx in range(levels.size):
                if power[idx+1] >= levels[idx]:
                    levels[idx] = power[idx+1]
                else:
                    levels[idx] -= 0.2

            for col in range(7):
                for row in range(7):
                    if levels[col] >= row+1:
                        lights[6-row, col] = colours[row]
                    else:
                        lights[6-row, col] = (0, 0, 0)

            yield lights, 0.030

    def update(self):
        return self.gen.__next__()

