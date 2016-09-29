import serial
import time

from qdsply import Qdsply
from dbi import Dbi

def milli(): # integer time in milliseconds
    return int(time.time() * 1000)

def checkbrk(a=True): # check breakbeam
    return False

BRKSPAN = 500 # debounce time for breakbeams
STPSPAN = 100 # time between animation steps
QSPAN = 18 * 10**5 # (30 mins) time between questions
HBSPAN = 6 * 10**4 # (1 min) time between heartbeats

qd = Qdsply() # question display to manage flipdot displays
dbi = Dbi() # database interface

lstbrk_a = None # last breakbeam a timestamp
lstbrk_b = None # last breakbeam b timestamp
lststp = None # last question animation step
lstnwq = None # last new question
lsthb = None # last heartbeat

qid = None

with serial.Serial("/dev/ttyUSB0", 57600) as srl:

    lstbrk_a = lstbrk_b = lststp = lstnwq = lsthb = milli() # init timestamps
    
    # init question
    qid, q, a, b = dbi.getNextQuestion()
    qd.ask(q, a, b)

    qd.wipe(srl, True) # wipe displays all white on startup
    time.sleep(0.5)

    qd.wipe(srl, False) # wipe displays all black
    time.sleep(0.5)

    while True:

        now = milli()

        if now - lstbrk_a > BRKSPAN:
            if checkbrk(True):
                lstbrk_a = now
                ratio = dbi.addVote(qid, True)
                qd.vote(True, ratio)

        if now - lstbrk_b > BRKSPAN:
            if checkbrk(False):
                lstbrk_b = now
                ratio = dbi.addVote(qid, False)
                qd.vote(False, ratio)

        if now - lstnwq > QSPAN:
            lstnwq = now
            qid, q, a, b = dbi.getNextQuestion()
            qd.ask(q, a, b)

        if now - lsthb > HBSPAN:
            lsthb = now
            dbi.logQuestion(qid)

        if now - lststp > STPSPAN:
            lststp = now
            qd.step(srl)

