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

def callback(indata, frames, time, status):
    if status:
        text = ' ' + str(status) + ' '
        print('\x1b[34;40m', text.center(bins, '#'),
                '\x1b[0m', sep='')
    if any(indata):
        magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
        magnitude *= gain / fftsize

        vals = magnitude[low_bin:low_bin + bins]
        screen.feed(vals)
        
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