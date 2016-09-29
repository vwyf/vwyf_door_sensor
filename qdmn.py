from __future__ import division

import serial
import time
from flipd.dsply import Dsply
from flipd.dotbf import Dotbf

class Qdmn:

    def __init__():

        # left & right displays
        self.lftd = Dsply([1, 2, 3, 4])
        self.rtd = Dsply([5, 6, 7, 8])

        # buffers
        self.qbf = None # question buffer
        self.lftbf = Dotbf(self.lftd.wdth, self.lftd.hght)
        self.rtbf = Dotbf(self.rtd.wdth, self.rtd.hght)
        self.abf = None
        self.bbf = None
        self.bgbf = Dotbf(self.lftd.wdth, self.lftd.hght * 2)

        ### states
        # 1 - qscroll
        # 2 - postqpause
        # 3 - vscroll
        # 4 - vpause
        # 5 - nvscroll
        # 6 - preqpause

        self.hasq = False
        self.qscroll = 0
        self.vscroll = 7

        self.adpth = 0 # depth of a vote buzzer
        self.bdpth = 0 # depth of b vote buzzer

    def step(self, srl):
        """step animation forwards"""


    def ask(self, q, a, b):
        """ask new question"""
        qbf = Dotbf(txt=q)
        if qbf.wdth < self.lftd.wdth:
            dlta = self.lftd.wdth - qbf.wdth
            self.qbf = Dotbf(self.lftd.wdth)
            qbf.writebf(self.qbf, dlta // 2, 0)
            self.qscroll = 0
        else:
            self.qbf = qbf
            self.qscroll = self.qbf.wdth - self.lftd.wdth


    def vote(self, a=True, dpth=10):
        """add depth to a or b vote buzzer"""


