# library for flipdot display buffer
import math
import font

class Display:

    def __init__(ads, pwidth=28, pheight=7):
        self.ads = [int(address) for address in ads]
        self.pwidth = 28 # panel width
        self.pheight = 7 # panel height

        self.bfs = {} # buffers
    
    def render(srl, bfname, x, y): # render from given buffer at given origin


