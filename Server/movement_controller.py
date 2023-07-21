import socket
import threading
import time
from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

hipGPIO = 27
armGPIO = 17
hipPWMfactory = PiGPIOFactory()
armPWMfactory = PiGPIOFactory()
hipServo = Servo(hipGPIO, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=hipPWMfactory)
armServo = Servo(armGPIO, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=armPWMfactory)

#change to face pos!!!!
def move(pacePos):
	
	#temp!!!!
	left, right, down, up = pacePos
	
	if left > 0: 
		hipServo.min()
		
	if right > 0:
		hipServo.max()
		
	if down > 0: 
		armServo.min()
		
	if up > 0:
		armServo.max()
		
	'''while True
	
	#center pos
	centerX = 
	#face pos
	
	# if below: move down
	# repeat for every dir
	'''
