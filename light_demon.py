import RPi.GPIO as GPIO

sPin = 17 # GPIO17 - sensor
lPin = 27 # GPIO27 - led

# pin setup
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(sPin, GPIO.IN)
GPIO.setup(lPin, GPIO.OUT)

try:
	while 1:
		if GPIO.input(sPin): # button is released
			print("pew pew")
			GPIO.output(lPin, GPIO.LOW)
		else: # button is pressed:
			print(".")
			GPIO.output(lPin, GPIO.HIGH)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	GPIO.cleanup() # cleanup all GPIO