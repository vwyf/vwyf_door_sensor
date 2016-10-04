from __future__ import division
from enum import Enum

from flipd.dsply import Dsply
from flipd.dotbf import Dotbf

class Qst(Enum): # question state
    qscroll = 1
    postqpause = 2
    vscroll = 3
    vpause = 4
    nvscroll = 5
    preqpause = 6
    noq = 7

class Qdsply:

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
        self.lftrtiobf = Dotbf(self.lftd.wdth, self.lftd.hght)
        self.rtrtiobf = Dotbf(self.rtd.wdth, self.rtd.hght)

        ### states
        self.qst = Qst.noq # question state
        self.vst = False # vote buzzer state

        self.adpth = 0 # depth of a vote buzzer
        self.bdpth = 0 # depth of b vote buzzer
        self.rtio = 0.5

        self.qscroll = 0
        self.mxqscroll = 0
        self.vscroll = 0
        self.mxvscroll = 7

    def step(self, srl):
        """step animation forwards"""

        if self.qst == Qst.noq:
            self.wipe(srl, False)
            return

        if self.vst:
            if self.adpth > 0 or self.bdpth > 0:
                self._render_ratio()
            else:
                self.vst = False
                return
            
            if self.adpth > 0:
                self.adpth -= 1
                self._buzza()

            if self.bdpth > 0:
                self.bdpth -= 1
                self._buzzb()

            self.lftd.render(srl, self.lftrtiobf)
            self.rtd.render(srl, self.rtrtiobf)
            return

        if self.qst == Qst.qscroll:
            if self.qscroll == 0:
                self.qst = Qst.vscroll
                return

            self.qscroll -= 1
            self.lftd.render(srl, bgbf, self.qscroll, self.vscroll)
            self.rtd.render(srl, bgbf, self.qscroll, self.vscroll)
            return

        if self.qst == Qst.vscroll:
            if self.vscroll == self.mxvscroll:
                self.qscroll = self.mxqscroll
                self.qst = Qst.nvscroll
                return

            self.vscroll += 1
            self.lftd.render(srl, bgbf, self.qscroll, self.vscroll)
            self.rtd.render(srl, bgbf, self.qscroll, self.vscroll)
            return
        
        if self.qst == Qst.nvscroll:
            if self.vscroll == 0:
                self.qst = Qst.qscroll
                return

            self.vscroll -= 1
            self.lftd.render(srl, bgbf, self.qscroll, self.vscroll)
            self.rtd.render(srl, bgbf, self.qscroll, self.vscroll)
            return                      


    def _buzza(self):
        aw = self.abf.wdth
        ldw = self.lftd.wdth
        lap = ((ldw // 2) - aw) // 2
        self.abf.flipmask(self.lftrtiobf, lap, 0)

        rdw = self.rtd.wdth
        rap = (rdw // 2) + (((rdw // 2) - aw) // 2)
        self.abf.flipmask(self.rtrtiobf, rap, 0)

    def _buzzb(self):
        bw = self.bbf.wdth
        ldw = self.lftd.wdth
        lbp = (ldw // 2) + (((ldw // 2) - bw) // 2)
        self.bbf.flipmask(self.lftrtiobf, lbp, 0)

        rdw = self.rtd.wdth
        rbp = ((rdw // 2) - bw) // 2
        self.bbf.flipmask(self.rtrtiobf, rbp, 0)


    def _render_ratio(self):
        llst = self.lftd.wdth // self.rtio
        for x in range(self.lftd.wdth):
            on = x < llst
            for y in range(self.lftd.hght):
                self.lftrtiobf[x, y] = on

        rlst = self.rtd.wdth // self.rtio
        for x in range(self.lftd.wdth):
            on = x >= llst
            for y in range(self.lftd.hght):
                self.lftrtiobf[x, y] = on


    def ask(self, q, a, b):
        """ask new question"""
        qbf = Dotbf(txt=q)
        if qbf.wdth < self.lftd.wdth:
            dlta = self.lftd.wdth - qbf.wdth
            self.qbf = Dotbf(self.lftd.wdth)
            qbf.writebf(self.qbf, dlta // 2, 0)
            self.mxqscroll = 0
        else:
            self.qbf = qbf
            self.mxqscroll = self.qbf.wdth - self.lftd.wdth

        self.qscroll = self.mxqscroll

        self.abf = Dotbf(txt=a)
        self.bbf = Dotbf(txt=b)

    def vote(self, a, ratio, dpth=10): # a -> bool, true if vote is for a
        """add depth to a or b vote buzzer"""
        self.rtio = ratio
        self.vst = True
        if a:
            self.adpth += dpth
        else:
            self.bdpth += dpth

    def wipe(self, srl, white=True):
        Dsply.WIPE(srl, white)