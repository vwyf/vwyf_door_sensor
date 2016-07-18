import RPi.GPIO as GPIO

sPin = 17 # GPIO17

# pin setup
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(sPin, GPIO.IN)

try:
    while 1:
        if GPIO.input(sPin): # button is released
            print("pew pew")
        else: # button is pressed:
            print(".")
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO