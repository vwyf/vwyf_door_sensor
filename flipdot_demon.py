### flipdot display
###
### 0:1200
### 1:2400
### 2:4800
### 3:9600 <--- this should be set, means 1-ON 2-ON 3-OFF
### 4:19200 
### 5:38200 <-- do not use, most probably wrong speed programmed
### 6: 9600
### 7: 9600
### 8: 9600
###
### 0x80 beginning 
###___________________
### 0x81 - 112 bytes / no refresh / C+3E
### 0x82 - refresh
### 0x83 - 28 bytes of data / refresh / 2C
### 0x84 - 28 bytes of data / no refresh / 2C
### 0x85 - 56 bytes of data / refresh / C+E
### 0x86 - 56 bytes of data / no refresh / C+E
### ---------------------------------------
### address or 0xFF for all
### data ... 1 to number of data buytes
### 0x8F end

import serial
import time

SCROLL_PAUSE = 0.1
PANEL_WIDTH = 28
question_string = "VOTE EARLY VOTE OFTEN -"

font = {
    ' ': bytearray([0]),
    '+': bytearray([24,  126, 126,  24,  0]),
    '-': bytearray([24,   24,  24,  24,  0]),
    '0': bytearray([62,   65,  65,  62,  0]),
    '1': bytearray([0,   66,  127, 64,  0]),
    '2': bytearray([98,   81,  73,  70,  0]),
    '3': bytearray([34,   65,  73,  54,  0]),
    '4': bytearray([56,   36,  34, 127, 32]),
    '5': bytearray([79,   73,  73,  49,  0]),
    '6': bytearray([62,   73,  73,  50,  0]),
    '7': bytearray([3,    1,   1, 127,  0]),
    '8': bytearray([54,   73,  73,  54,  0]),
    '9': bytearray([38,   73,  73,  62,  0]),
    'A': bytearray([0x3C, 0x0A, 0x0A, 0x3C]),
    'B': bytearray([0x3E,0x2A,0x2A,0x14]),
    'C': bytearray([0x1C,0x22,0x22,0x14]),
    'D': bytearray([0x3E,0x22,0x22,0x1C]),
    'E': bytearray([0x3E,0x2A,0x2A]),
    'F': bytearray([0x3E,0x0A,0x0A]),
    'G': bytearray([0x1C,0x22,0x2A,0x2A]),
    'H': bytearray([0x3E,0x08,0x08,0x3E]),
    'I': bytearray([0x3E]),
    'J': bytearray([0x10,0x20,0x20,0x1E]),
    'K': bytearray([0x3E, 0x08, 0x14, 0x22]),
    'L': bytearray([0x3E,0x20,0x20]),
    'M': bytearray([0x3E,0x04,0x08,0x04]),
    'N': bytearray([0x3E,0x04,0x08,0x3E]),
    'O': bytearray([0x1C,0x22,0x22,0x1C]),
    'P': bytearray([0x3E,0x0A,0x0A,0x1C,0x04]),
    'Q': bytearray([0x1C,0x22,0x12,0x2C]),
    'R': bytearray([0x3E,0x0A,0x1A,0x24]),
    'S': bytearray([0x24,0x2A,0x2A,0x12]),
    'T': bytearray([0x02,0x02,0x3E,0x02,0x02]),
    'U': bytearray([0x1E,0x20,0x20,0x1E]),
    'V': bytearray([0x06,0x18,0x20,0x18,0x6]),
    'W': bytearray([0x1E,0x20,0x1E,0x20,0x1E]),
    'X': bytearray([0x36,0x08,0x08,0x36]),
    'Y': bytearray([0x2E,0x28,0x28,0x1E]),
    'Z': bytearray([0x32,0x2A,0x2A,0x26])
}

transmission = bytearray([
    0x80, #header
    0x83, # 28 bytes, refresh
    0x01, # address
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 28 bytes data
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x8F #EOT
])

all_bright = bytearray([
    0x80,  # header
    0x83,  # 28 bytes refresh
    0xFF,  # address
    0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, # 28 bytes data
    0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F,
    0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F,
    0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 
    0x8F # EOT
])

all_dark = bytearray([
    0x80,  #header
    0x83,  # 28 bytes refresh
    0xFF,  # address
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # 28 bytes data
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x8F # EOT
])

def show_slice(panel_address, t, srl, question):
    transmission = bytearray([
        0x80, #header
        0x83, # 28 bytes, refresh
        panel_address, # address
    ])
    
    for i in range(t, t + 28): # 28 bytes data
        transmission.append(question[i%len(question)])
        
    transmission.append(0x8F) # EOT

    srl.write(transmission)

# loop over question string and add columns to question
question = bytearray()
for c in question_string:
    if c in font:
        question.extend(font[c])
        question.append(0) # put space between letters

# if question is fewer than 28 columns pad it out with spaces
while len(question) < PANEL_WIDTH:
    question.extend(font[' '])

t = 0
         
with serial.Serial("/dev/ttyUSB0", 9600) as srl:

    srl.write(all_bright)
    time.sleep(0.5)

    srl.write(all_dark)
    time.sleep(0.5)

    while True:

        show_slice(1, t, srl, question)
        time.sleep(SCROLL_PAUSE)

        t = t + 1
        if t >= len(question):
            t = 0
