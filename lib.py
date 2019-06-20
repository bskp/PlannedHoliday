#!/usr/bin/env python3

import socket
from time import sleep
from PIL import Image

class SevenBySeven:
    def __init__(self, ip="holiday-ac2d8f.local", port=9988):
        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        self.target = (ip, port)

    def send(self, img):
        # check image
        if img.size is not (7, 7):
            img = img.resize( (7, 7) )

        if img.mode is not 'RGB':
            img = img.convert('RGB')

        # assemble packet data
        packet = bytes(10) + bytes(3)
        
        for idx in range(49):
            y = 6 - idx/7
            x = idx%14

            if x > 6: 
                x = 13 - x

            r, g, b = img.getpixel((x, y))
            packet += bytes( (r, g, b) )

        self.sock.sendto(packet, self.target)


fixpoint = lambda val: val  #nop.
def hsvTransform(img, h=fixpoint, s=fixpoint, v=fixpoint):
    ''' Apply a transformation (given as a lambda expression) to an images H/S/V channels '''

    hues, sats, vals = img.convert('HSV').split()
    hues = hues.point(h)
    sats = sats.point(s)
    vals = hues.point(v)

    return Image.merge('HSV', (hues, sats, vals))


if __name__ == '__main__':
    screen = SevenBySeven('0.0.0.0')
    img = Image.open('images/rainbow.png')
    img = img.convert('HSV')

    hue_shift = 0
    while True:
        c = hsvTransform(img, h=lambda val: val + hue_shift)
        screen.send(c)

        print('.', sep='', end='', flush=True)
        hue_shift += 1
        sleep(0.3)
