#!/usr/bin/env python3

import time
from lib import *
from remote import AppleRemote, buttons
import subprocess

screen = SevenBySeven()

back_to_menu = False

def handler(btn):
    global back_to_menu
    if btn == buttons.menu:
        back_to_menu = True

ar = AppleRemote()
ar.attach_handler(handler)
ar.attach_handler(print)

def menu(item):
    cs = 'yellow', 'blue', 'red', 'green', 'magenta', 'cyan'
    m = load('menu')
    m.putpixel( (item+1, 3), ImageColor.getrgb( cs[item] ) )
    return m

with ar:
    selected = 0
    while True:
        i = 0

        # decide upon new process to run
        app = 'trainride.py'
        apps = {
            0: 'trainride.py',
            1: 'eq.py',
            2: 'flame.py',
            3: 'gol.py',
            4: 'sprite.py'
            }

        labels = 'Travelling', 'Spectrum', 'Flame', 'Game of Life', 'Pixel Art'

        screen.show(monochrome('black'))
        screen.fade(menu(selected), 0.3)
        while True:
            screen.show(menu(selected))

            btn = ar.await_btn()
            if btn == buttons.center:
                break

            if btn == buttons.left and selected > 0:
                selected = selected - 1

            if btn == buttons.right and selected < len(apps) - 1:
                selected = selected + 1

            if btn == buttons.down or btn == buttons.up:
                screen.write(labels[selected])


        print(btn)
        screen.fade(monochrome('black'), 0.3)

        p = subprocess.Popen(('python', apps[selected]))

        back_to_menu = False
        while not back_to_menu:
            time.sleep(0.2)
            print(i)
            i = i + 1

        p.terminate()
        p.wait()
