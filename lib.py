#!/usr/bin/env python3

import socket
import glob
from time import sleep
from functools import reduce
from random import shuffle

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

# Helpers


_fnt = ImageFont.truetype('fonts/pixelmix.otf', 8)

def load(filename):
    matches = glob.glob('images/' + filename + '*')
    return Image.open( matches[0] )


def write(text):
    size = 1000, 7 
    canvas = Image.new('RGB', size)
    d = ImageDraw.Draw(canvas)
    d.text( (1, -1), text, font=_fnt)
    size = d.textsize(text, _fnt)
    return canvas.crop((0, 0, size[0] + 7, 7))


def monochrome(color):
    return Image.new('RGB', (7, 7), color)


def mix(*images):
    return reduce(ImageChops.screen, images)


class SevenBySeven:
    ''' Abstraction for light-chain-based low resolution display, connected over UDP. '''
    def __init__(self, ip="holiday-ac2d8f.local", port=9988):
        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        self.target = (ip, port)
        self.show( monochrome('black') )


    def _map(self, idx):
        y = 6 - int (idx/7)
        x = idx%14

        if x > 6: 
            x = 13 - x
        
        return x, y


    def show(self, img):
        ''' Send a new 7-by-7 image to the screen. No guarantees about delay and success. '''

        def _gamma(val):
            val = val/0xFF
            val = val**2
            return int(val*0xFF)

        if isinstance(img, str):
            img = load(img)

        # check image
        if img.mode is not 'RGB':
            img = img.convert('RGB')

        # assemble packet data
        packet = bytes(10) + bytes(3)
        
        for idx in range(49):
            x, y = self._map(idx)

            r, g, b = img.getpixel((x, y))
            r = _gamma(r)
            g = _gamma(g)
            b = _gamma(b)
            packet += bytes( (r, g, b) )

        self.current = img
        self.sock.sendto(packet, self.target)

    def fade(self, img, duration=1, hz=50):
        current = self.current.copy()
        for t in np.linspace(0, 1, duration*hz):
            self.show( Image.blend(current, img, t) )
            sleep(1/hz)


    def pan(self, img, duration=1, substeps=8):
        width, height = img.size

        all = Image.new('RGB', (7 + width, height) )
        all.paste(self.current)
        all.paste(img, (7, 0) )
        all = all.resize( ( all.size[0]*substeps, 7))

        steps = width*substeps
        for step in range(1, steps + 1):
            view = all.crop( (step, 0, step + 7*substeps, 7 ) ) 
            self.show( view.resize( (7, 7), Image.BICUBIC) )
            sleep(duration/steps)



    def _reveal_by_pixel(self, img, duration, order):
        for idx in order:
            pos = self._map(idx)
            self.current.putpixel(pos, img.getpixel(pos) )
            self.show(self.current)
            sleep(duration/49)


    def snake(self, img, duration=1):
        self._reveal_by_pixel(img, duration, range(49))

    def dissolve(self, img, duration=1):
        order = list(range(49))
        shuffle(order)
        self._reveal_by_pixel(img, duration, order)


    def write(self, text, speed=1):
        rendered = write(text)
        self.pan(rendered, rendered.size[0]/15*speed, 2)



def hsvTransform(img, h=None, s=None, v=None):
    ''' Apply a transformation (given as a lambda expression) to an image's H/S/V channels. '''

    hues, sats, vals = img.convert('HSV').split()
    if h: hues = hues.point(h)
    if s: sats = sats.point(s)
    if v: vals = hues.point(v)

    return Image.merge('HSV', (hues, sats, vals))




if __name__ == '__main__':
    screen = SevenBySeven()

    while True:
        screen.write('Game of Life: Start now!')
        screen.fade( load('rainbow'), 2)
        screen.pan( load('tot'), 1)
        screen.snake( monochrome('blue') )
        screen.dissolve( monochrome('magenta') )