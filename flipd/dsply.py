# library for flipdot display buffer
import math

from frm import Frm

class Dsply:

    @staticmethod
    def WIPE(srl, white):
        """wipe all displays"""
        srl.write(Frm(white=white))

    def __init__(adrss):
        self.adrss = [int(a) for a in adrss]
        self.lft = lft # a is on left
        self.wdth = Frm.WDTH * len(self.adrss)
        self.hght = Frm.HGHT # panel height
    
    def render(srl, bf, x=0, y=0): # render from given buffer at given origin

        for i, adrs in enumerate(self.adrss):
            f = Frm(adrs)
            bf.writefrm(f, x + (i * Frm.WDTH), y)
            srl.write(f.b)




