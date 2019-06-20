#!/usr/bin/env python3

from time import sleep
from lib import SevenBySeven
from sprite import Sprite


mervin = Sprite('images/mervin.png', 8)
screen = SevenBySeven()
mervin.define('walk_right', range(3))

while True:
    screen.send( mervin.walk_right() )
    sleep(0.1)
    