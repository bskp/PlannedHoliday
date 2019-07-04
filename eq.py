import math

import numpy as np
import sounddevice as sd
from lib import *

screen = SevenBySeven()
samplerate = sd.query_devices(None, 'input')['default_samplerate']

low, high = (100, 4000)
bins = 7 
gain = 100
block_duration = 20 #ms

delta_f = (high - low) / (bins - 1)
fftsize = math.ceil(samplerate / delta_f)
low_bin = math.floor(low / delta_f)

normalization_tau = 4 # seconds
d = block_duration/normalization_tau/1000

avgs = np.ones(7)/gain

colors = 'black', 'blue', 'cyan', 'yellow', 'red'

def callback(indata, frames, time, status):
    global avgs

    if any(indata):

        ramp = np.linspace(0.0, 1.0, 7)
        #ramp = np.sqrt(ramp)
        ramp = ramp - 1
        ref = ramp.reshape((7,1)).repeat(7, axis=1)

        magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))

        vals = magnitude[low_bin:low_bin + bins] / fftsize
        avgs = avgs*(1 - d) + d*vals
        normalized = vals/avgs*0.25

        i = gradient_map(ref + normalized, colors)
        old = decay(screen.current, 0.1)
        i = mix(old, i)

        for ch in avgs:
            print("%4.0f " % (ch*1000), end='')
        print()

        screen.show(i)


        #flatten out averages
        #avgs = np.ones(7)*np.average(avgs)

        
    else:
        print('no input')

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