import pyglet
import numpy as np
import matplotlib
#matplotlib.use('AGG')
import matplotlib.pyplot as plt

fpath = "/home/adam/Music/Anamanaguchi/PopIt.wav"

f = pyglet.media.load(fpath, streaming=False)
sr = f.audio_format.sample_rate
d = np.fromstring(f._data, dtype=np.int16).reshape((-1, 2)).astype(np.float)
d = np.sum(d, axis=1) / 65536.0

bins, freqs, Pxx, im = plt.specgram(d[sr*20:sr*22])

h = im.get_array()
h += h.min()
h /= h.max()
h = 1.0 - h
h *= 255.0
h = np.uint8(h[::-1])

print(h)
print(h.shape)
print(h.min())
print(h.max())

#height, width, channels = h.shape
height, width = h.shape

window = pyglet.window.Window(width=width, height=height)
imagedata = pyglet.image.ImageData(width, height, 'I', bytes(h.data))


@window.event
def on_draw():
    window.clear()
    imagedata.blit(0, 0)

pyglet.app.run()
