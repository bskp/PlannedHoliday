#!/usr/bin/env python3

from lib import SevenBySeven
import pyautogui
from PIL import ImageGrab, Image
import subprocess
import os
import tempfile

screen = SevenBySeven()

fh, filepath = tempfile.mkstemp(".png")
os.close(fh)

def start_capture():
    return subprocess.Popen(["screencapture", "-x", filepath])

process = start_capture()
process.wait()

g = None

x_, y_ = 0, 0
while True:

    if process is not None and process.poll() is not None:
        g = Image.open(filepath)
        print('x', sep='', end='', flush=True)
        os.unlink(filepath)
        process = None

    x, y = pyautogui.position()
    if x == x_ and y == y:
        if process is None:
            process = start_capture()

    x_, y_ = x, y

    x = x*2
    y = y*2
    r = 20

    gg = g.crop( (x-r, y-r, x+r+1, y+r+1) )

    screen.show(gg.resize((7,7), Image.BICUBIC))
    print('.', sep='', end='', flush=True)