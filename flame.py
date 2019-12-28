import math

import numpy as np
import sounddevice as sd
from lib import *

screen = SevenBySeven()
samplerate = sd.query_devices(None, 'input')['default_samplerate']

low, high = (100, 4000)
bins = 7 
gain = 200
block_duration = 80 #ms

delta_f = (high - low) / (bins - 1)
fftsize = math.ceil(samplerate / delta_f)
low_bin = math.floor(low / delta_f)

normalization_tau = 4 # seconds
d = block_duration/normalization_tau/1000

avgs = np.ones(7)/100  # initial values

colors = 'black', 'black', 'brown', 'red', 'orange', 'yellow'

def callback(indata, frames, time, status):
    if not any(indata): 
        return

    global avgs

    magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
    vals = magnitude[low_bin:low_bin + bins] / fftsize

    avgs = avgs*(1 - d) + d*vals
    normalized = vals/avgs*0.4

    faint = decay(screen.current, 0.2)
    sparkles = gradient_map( np.random.rand(7,7)*0.15, ('black', 'orange') )
    faint = mix(faint, sparkles)
    screen.show( faint )
    screen.feed(normalized, colors)

    for ch in avgs:
        print("%4.0f " % (ch*1000), end='')
    print()


with sd.InputStream(device=None, channels=1, callback=callback,
                    blocksize=int(samplerate * block_duration / 1000),
                    samplerate=samplerate):
    while True:
        response = input()
        if response in ('', 'q', 'Q'):
            break
        for ch in response:
            if ch == '+':
                gain *= 2
            elif ch == '-':
                gain /= 2