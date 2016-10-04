import serial
import time

from qdsply import Qdsply
from dbi import Dbi

def milli(): # integer time in milliseconds
    return int(time.time() * 1000)

def checkbrk(srl): # check breakbeam
    brk = srl.read()
    if brk == ord("a"):
        return True, True # gateway a break
    if brk == ord("b"):
        return True, False # gateway b break
    return False, True # no break event

STPSPAN = 100 # time between animation steps
QSPAN = 18 * 10**5 # (30 mins) time between questions
HBSPAN = 6 * 10**4 # (1 min) time between heartbeats

qd = Qdsply() # question display to manage flipdot displays
dbi = Dbi() # database interface

lststp = None # last question animation step
lstnwq = None # last new question
lsthb = None # last heartbeat

qid = None

with serial.Serial("/dev/ttyUSB0", 57600) as dsply_srl:
    with serial.Serial("/dev/ttyUSB1", 57600, timeout=0.01) as brk_srl:

        lststp = lstnwq = lsthb = milli() # init timestamps
        
        # init question
        qid, q, a, b = dbi.getNextQuestion()
        qd.ask(q, a, b)

        qd.wipe(srl, True) # wipe displays all white on startup
        time.sleep(0.5)

        qd.wipe(srl, False) # wipe displays all black
        time.sleep(0.5)

        while True:

            # check breakbeam serial for votes
            has, a = checkbrk(brk_srl)
            if has:
                ratio = dbi.addVote(qid, a)
                qd.vote(a, ratio)

            # do stuff when its time
            now = milli()

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

