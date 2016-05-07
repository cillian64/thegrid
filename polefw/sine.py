import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
import matplotlib.pyplot as plt
import serial
import sys

ser = serial.Serial("/dev/ttyUSB0", 115200)

import time
time.sleep(1)

#t = np.linspace(0, 3, 11520*3)
#x = np.sin(2*np.pi*4000*t)
#v = (x * 15) + 65
#ser.write(v.astype(np.uint8))

#while True:
    #for dur in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        #sq = np.repeat([255,0]*(3000//dur), dur).astype(np.uint8)
        #ser.write(list(sq))
#sys.exit()

# Usable linearish range 50-80 in 8bit
# 200-320 in 10bit is 120 counts is ~128 is ~7 bits, nice
# 800 to 1280 in 12bit is 480 counts (!) is ~512 counts
# So take input bit, shift left by one, add 800
# Output is 784 to 1296

#x = 50
#while True:
#    print("x =", x)
#    ser.write([x, x, x, 0, 0, 0]*(11520//4))
#    x += 3
#    if x > 80:
#        x = 50

rate, wav = wavfile.read(sys.argv[1])
wav = resample(wav, int(11520*(wav.size / rate))).astype(np.int16)
wav /= 512
wav += 127
print(min(wav), max(wav))
wav = np.clip(wav, 0, 255).astype(np.uint8)
#wavfile.write("/tmp/testing2.wav", 11520, wav)
ser.write(wav)
#plt.plot(wav[:11520])
#plt.show()
