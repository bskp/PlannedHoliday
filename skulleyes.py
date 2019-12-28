from lib import *
from sprite import Sprite

skull = Sprite('images/hatspin.gif')
screen = SevenBySeven()

skull.define('look', range(4) )

while True:
    screen.show( skull.look() )
    sleep(0.2)