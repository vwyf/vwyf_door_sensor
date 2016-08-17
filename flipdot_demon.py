### TMS Hyperloop display
### increase of 2 x 2  pos XY5 counter as a result of passing a car
### 
### Arduino Due
### rs485 brakout 
### connections:
### Breakout - Arduino
### GND  -   GND 
### RTS  -   3V3
###TX-O  -   not connected
###RX-I  -   TX (pin 1 digital)
###3-5V  -   5V
### radar switch#1
### between  pin 3 and GND
### radar switch@2
### between pin4 and GND
###
### deboucing of a trigger button every  5s
### dipswitches settings of the lsb controller
### 3 positions: speed of communication:
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
### 5 positions: order.
### digit 1: 1
### digit 2: 2
### digit 3: 3
### ... etc digit 9: 9
##
### switch#1 is shown on digit 1 and 2 / switch #2 is shown on digit 3 and 4
##
##
##
##
### pin 2 digital connected through 10kohm res to 5V and through a radar to GND - Interrupt 0 is on DIGITAL PIN 2!
### pin 3 digitial connected though 10 kohm res to 5V and through a radar to GND - Interr 1 is on digital pin 3
##
##
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
### data ... 1 to nuber of data buytes
### 0x8F end

import serial
import time

### do we need to do this with usb board???
# volatile int state = LOW;      # The input state toggle

numbers = bytearray([
    62,   65,  65,  62,  0, # 0
    0,   66,  127, 64,  0,  # 1
    98,   81,  73,  70,  0, # 2
    34,   65,  73,  54,  0, # 3
    56,   36,  34, 127, 32, # 4
    79,   73,  73,  49,  0, # 5
    62,   73,  73,  50,  0, # 6
    3,    1,   1, 127,  0,  # 7
    54,   73,  73,  54,  0, # 8
    38,   73,  73,  62,  0, # 9
    24,  126, 126,  24,  0, # +
    24,   24,  24,  24,  0  # -
])

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


def show_number(panel_address, number_to_show, srl): # byte, int

    cyfra1 = 0;
    cyfra2 = 0;

    cyfra1 = number_to_show / 10
    cyfra2 = number_to_show - (cyfra1 * 10)


    transmission[2] = panel_address;
    for t in range(0, 5):
        transmission[10+3+t] = numbers[(cyfra1*5)+t]
        
    for t in range(0, 5):
        transmission[15+3+t]= numbers[(cyfra2*5)+t];

    for t in range(0, 5):
        transmission[3+t]= numbers[((9+panel_address)*5)+t]; # +

    srl.write(transmission)
    
#int pin1 = 2;
#int pin2 = 3;

counter1 = 0x00
counter2 = 0x00

n = 0
         
with serial.Serial("/dev/ttyUSB0", 9600) as srl:

    while True:

        srl.write(all_bright)
        time.sleep(0.5)

        srl.write(all_dark)
        time.sleep(0.5)

        show_number(1, 0, srl)
        time.sleep(0.5)



##
##                  
##                  
##void setup() {
##
##Serial.begin(57600);  
##
##Serial.write(all_bright,32); 
##delay (250);
##Serial.write(all_dark,32); 
##delay (250);
##
##attachInterrupt(0, my_interrupt_handler1, LOW);
##attachInterrupt(1, my_interrupt_handler2, LOW);
##
##show_number(1,counter1);
##show_number(2,counter2);
##
##}
##

