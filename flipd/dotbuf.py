import math
import font

class Dotbuf:

    def __init__(self, wdth, hght):
        self.wdth = wdth
        self.hght = hght
        self._b = bytearray(math.ceil(wdth * hght / 8))

    def setdot(self, x, y, on): # set byte at offset
        x = x % self.wdth
        y = y % self.hght
        o = (x * 8) + y
        i = math.floor(o / 8)
        j = o % 8
        msk = 0x1 << j
        if on:
            self._b[i] |= msk # set bit j of byte i to 1
        else:
            self._b[i] &= ~msk # set bit j of byte i to 0

    def getdot(self, x, y):
        x = x % self.wdth
        y = y % self.hght
        o = (x * 8) + y
        i = math.floor(o / 8)
        j = o % 8
        msk = 0x1 << j
        return self._b[i] & j

    def writedotbuf(self, ox, oy, x, y, w, h, dbf): # write dotbuf values to other
        for u in range(x, x + w):
            for v in range(y, y + w):
                dbf.setdot(ox + u, oy + v, self.getdot(u, v))

    def writeframe(self, ox, oy, frm): # write buffer values to frame at offset
        for i, x in enumerate(range(ox, ox + frm.wdth)):
            clmn = 0
            for i, y in enumerate(range(oy, oy + frm.hght)):
                if self.getdot(x, y):
                    clmn |= 0x1 << j
            frm[i] = clmn

    def invert(self):
        for i in range(len(self._b)):
            self._b[i] = ~self._b[i] & 0xff

def textbuf(txt, fnt=font.XU):
    
    a = bytearray()
    for c in question_string:
        if c in font:
            a.extend(font[c])
            a.append(0)

    b = Dotbuf(len(a) - 1, 7)
    for x in range(b.wdth):
        for y in range(7):
            b.setdot(x, y, a[x] & 0x1 << y)

    return b