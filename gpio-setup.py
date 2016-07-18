# External module imports
import RPi.GPIO as GPIO
import time
import socket # socket communication with PD

# Pin Definitons:
pwmPin = 12 # GPIO18
ledPin = 16 # GPIO23
butPin = 11 # GPIO17

dc = 95 # duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
GPIO.setup(pwmPin, GPIO.OUT) # PWM pin set as output
pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency
GPIO.setup(butPin, GPIO.IN) # Button pin set as input

# Initial state for LEDs:
GPIO.output(ledPin, GPIO.LOW)
pwm.start(dc)

# print("Here we go! Press CTRL+C to exit")

def send2socket(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 3000)
        #print 'conneting to localhost:3000'
        sock.connect(server_address)
        sock.sendall(message)
    finally:
        sock.close()


try:
    while 1:
        send2socket(str(butPin) + " " + str(GPIO.input(butPin))+";") #send butPin value to PD
        if GPIO.input(butPin): # button is released
            pwm.ChangeDutyCycle(dc)
            GPIO.output(ledPin, GPIO.LOW)
        else: # button is pressed:
            pwm.ChangeDutyCycle(100-dc)
            GPIO.output(ledPin, GPIO.HIGH)
            time.sleep(0.075)
            GPIO.output(ledPin, GPIO.LOW)
            time.sleep(0.075)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    pwm.stop() # stop PWM
    GPIO.cleanup() # cleanup all GPIO




