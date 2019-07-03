#!/usr/bin/env python3

'''
Quick and dirty implementation of Conway's Game of Life.
'''

from lib import *
from PIL import Image, ImageChops
import numpy as np
from time import sleep
from random import randint
import collections
import itertools


# colors
gray = (0x70, 0x70, 0x70)
white = (0x90, 0x90, 0x90)
light = (0xff, 0xff, 0xff)
red = (0xff, 0, 0)
green = (0, 0xff, 0)

def sumNeighbours(x, y):
    def w(x, y):
        ''' Map acces with cyclic boundary conditions. '''
        return int(m[x%size[0], y%size[1]])

    return w(x-1, y-1) \
         + w(x-1, y  ) \
         + w(x-1, y+1) \
         + w(x  , y-1) \
         + w(x  , y+1) \
         + w(x+1, y-1) \
         + w(x+1, y  ) \
         + w(x+1, y+1)


def render(where, rgb_tuple=(0xFF, 0xFF, 0xFF) ):
    w = where.reshape(size[0], size[1], 1)
    c = np.uint8(rgb_tuple).reshape(1, 1, 3)
    return Image.fromarray(w*c, 'RGB' )


def init():
    m = np.zeros((7,7)) > 0

    while np.sum(m) < 20:
        x = randint(0, size[0] - 1)
        y = randint(0, size[1] - 1)
        if m[x,y]: continue

        m[x,y] = True
        after = render(m, gray)
        screen.fade(after, 0.1)
    
    sleep(0.5)
    brighter = render(m)
    screen.fade(brighter, 1)
    screen.fade(after, 0.5)

    return m

size = 7,7

screen = SevenBySeven()
sleep(0.1)
m = init()
history = collections.deque(maxlen=30)

reset = False
while True:
    # Calculate new generation
    m_ = m.copy()

    # Extinct?
    if np.sum(m) == 0:
        screen.fade(load('tot.png'), 2)
        m = init()

    # Pattern repeating?
    elif reset is True:
        screen.fade( load('infinite.png'), 2)
        sleep(1)
        m = init()
        reset = False

    for x in range(size[0]):
        for y in range(size[1]):
            s = sumNeighbours(x, y)
            if (m[x, y]):
                m_[x, y] = s is 2 or s is 3
            else:
                m_[x, y] = s is 3
        

    # Animate transition
    current = render(m, white)
    staying = render(m & m_, white)
    dying = render(m & ~m_, red)
    sprouting = render(~m & m_, green)
    new = render(m_, white)

    dt = 0.2
    screen.fade( mix(staying, dying), dt)
    screen.fade( mix(staying, dying, sprouting), dt)
    screen.fade( mix(staying, sprouting), dt)
    screen.fade( new, dt)

    for past in itertools.islice(history, 10, 30):
        if np.array_equal(past, m):
            reset = True

    history.append(m)
    m = m_
    print('.', sep='', end='', flush=True)