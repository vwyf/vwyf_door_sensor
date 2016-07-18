import RPi.GPIO as GPIO
import socket # socket communication with PD

sPin = 17 # GPIO17 - sensor
lPin = 27 # GPIO27 - led

pewpew = True
hassock = False

# pin setup
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(sPin, GPIO.IN)
GPIO.setup(lPin, GPIO.OUT)

try:
	while not hassock:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_address = ('localhost', 3000)
			print 'conneting to localhost:3000'
			sock.connect(server_address)
			hassock = True
		except socket.error, e:
			print(e)
	while 1:
		if GPIO.input(sPin): # button is released
			print("pew pew")
			GPIO.output(lPin, GPIO.LOW)
			pewpew = True
		else: # button is pressed:
			print(".")
			GPIO.output(lPin, GPIO.HIGH)
			if pewpew:
				pewpew = False
				sock.sendall("1 1;")

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	GPIO.cleanup() # cleanup all GPIO

finally:
        sock.close()
