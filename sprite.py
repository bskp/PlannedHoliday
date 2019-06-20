
#!/usr/bin/env python3
# vim: set fileencoding=utf-8

from PIL import Image
class Sprite:

    def __init__(self, filename, grid_size=7, ):
        self.src = Image.open(filename)
        self.gs = grid_size
        self.grid = ( 
            int(self.src.width/self.gs),
            int(self.src.height/self.gs)
        )


    def getFrame(self, idx):
        x = idx%self.grid[0]
        y = idx/self.grid[1]
        return self.src.crop( (x*self.gs, y*self.gs, (x+1)*self.gs, (y+1)*self.gs) )


    def define(self, label, frame_idxs):
        ''' 
        Define a new animation cycle, consisting of the passed frame indices -- accessible as an object method under the given label.
        '''

        # Define the closure
        step = 0
        def cycle():
            nonlocal step
            step += 1
            if step >= len(frame_idxs): step = 0
            return self.getFrame(frame_idxs[ step ])
            
        setattr(self, label, cycle)