
#!/usr/bin/env python3
# vim: set fileencoding=utf-8

from PIL import Image
from time import sleep

class Sprite:
    ''' 
    Collection of animation sprites, based on a single source image (spritesheet).
    This class provides the #define-method to create animation cycle methods (with internal counter).
    '''

    def __init__(self, filename, grid_size=7, offset=(0,0) ):
        self.offset = offset
        self.src = Image.open(filename)
        self.gs = grid_size
        self.grid = ( 
            int(self.src.width/self.gs),
            int(self.src.height/self.gs)
        )


    def getTile(self, idx):
        ''' Get the tile at the given index. The sprite's tiles are enumerated in a left-to-right, bottom-to-up fashion. '''
        ox, oy = self.offset
        x = idx%self.grid[0]
        y = int( idx/self.grid[0] )
        return self.src.crop((
            x*self.gs + ox, 
            y*self.gs + oy, 
            (x+1)*self.gs + ox, 
            (y+1)*self.gs + oy
            ))


    def define(self, label, frame_idxs):
        ''' 
        Define a new animation cycle, consisting of the passed frame indices -- accessible as an object method under the given label.
        '''

        # Define the closure
        step = 0
        def cycle():
            nonlocal step
            tile = self.getTile(frame_idxs[ step ])

            step += 1
            if step == len(frame_idxs): step = 0
            return tile
            
        setattr(self, label, cycle)


if __name__ == '__main__':
    from lib import SevenBySeven
    import keyboard

    mervin = Sprite('images/mervin.png', 8, (1, 1) )
    screen = SevenBySeven()

    mervin.define('walk_right', range(4) )
    mervin.define('walk_left', range(4, 8) )
    mervin.define('walk_down', range(8, 12) )
    mervin.define('walk_up', range(12, 16) )

    keyboard.add_hotkey('space', lambda key: print('asdf' + key))

    while True:
        for i in range(10):
            screen.show( mervin.walk_up() )
            sleep(0.1)
        for i in range(10):
            screen.show( mervin.walk_right() )
            sleep(0.1)
        for i in range(10):
            screen.show( mervin.walk_down() )
            sleep(0.1)
        for i in range(10):
            screen.show( mervin.walk_left() )
            sleep(0.1)
        