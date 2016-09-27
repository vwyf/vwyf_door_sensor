import math
import numpy as np

import font

class Dotbuf:

    def __init__(self, wdth=28, hght=7, txt=None, fnt=font.XU):

        if txt is not None:
            a = self._textarray(txt, font)

            self.wdth = len(a)
            self.hght = 7
            self._b = np.zeros((self.hght, self.wdth), dtype=np.bool)
            for x in range(wdth):
                for y in range(hght):
                    self._b[y, x] = a[x] & (0x1 << y)

        else:
            self.wdth = wdth
            self.hght = hght
            self._b = np.zeros((self.hght, self.wdth), dtype=np.bool)

    def __setitem__(self, dex, on):
        x, y = dex
        x %= self.wdth
        y %= self.hght
        self._b[y, x] = on

    def __getitem__(self, dex):
        x, y = dex
        x %= self.wdth
        y %= self.hght
        return self._b[y, x]

    def writedotbuf(self, othr, ox, oy, x, y, wdth, hght):
        othr._b[oy:oy+hght, ox:ox+wdth] = self._b[y:y+hght, x:x+wdth]

    def writeframe(self, frm, x, y):
        for i, x in enumerate(range(x, x + frm.wdth)):
            clmn = 0
            for i, y in enumerate(range(y, y + frm.hght)):
                if self[x, y]:
                    clmn |= 0x1 << j
            frm[i] = clmn

    def invert(self):
        self._b.invert()

    def _textarray(self, txt, fnt):
        
        a = bytearray([0])
        for c in txt:
            if c in font:
                a.extend(font[c])
                a.append(0)

        return a