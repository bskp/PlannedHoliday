from lib import *
from random import randint

screen = SevenBySeven()

full = load('nacht')
width, height = full.size

# the 'train window', which is the viewport to be panned across the full image.
window = int(width/20)

t = width/window/8
print("Pan duration: %ds" % t)
print("Window size: %dpx" % window)

while True:
    x = randint(0, height - window)
    print("Pan height: %2.0f%%" % (x/height*100) )
    stripe = full.crop( (0, x, width, x + window) )
    stripe = stripe.resize( (int(7/window*width), 7), Image.BICUBIC )
    screen.pan(stripe, t, 4)