#!/usr/bin/python
# -*- coding:utf-8 -*-

##
# Most of the core code in this file was taken from the "Line_Follow.py" (Especially the math logic) which is part of the demo code distributed for the Alphabot PiZero by WaveShare.
# Also, this file makes use of another file called TRSensors.py, which is also included in the Waveshare demo code package.
#######

import RPi.GPIO as GPIO

# from AlphaBot2 import AlphaBot2
from DCMotors_VS.py import DCMotors

from TRSensors import TRSensor
import time

Button = 7

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Button,GPIO.IN,GPIO.PUD_UP)

# maximum = 100;
maximum = 30;
integral = 0;
last_proportional = 0;

TR = TRSensor() # create a new instance of the Tracking Sensor class
# Ab = AlphaBot2()
DCM = DCMotors() # create a new instance of the DC Motors (Variable Speed) class

### STEP 1 | Waiting to begin calibration sequence
DCM.stop() # initally, we must set the DC motors to halt/stop
print("Waiting to initiate calibration sequence")
time.sleep(2)

### STEP 2 | Calibration sequence
for i in range(0,100):
	if(i<25 or i>= 75):
		Ab.right()
		Ab.setPWMA(30)
		Ab.setPWMB(30)
	else:
		Ab.left()
		Ab.setPWMA(30)
		Ab.setPWMB(30)
	TR.calibrate()
DCM.stop()
print(TR.calibratedMin)
print(TR.calibratedMax)

### STEP 3 | Wait for the user to toggle the onboard button
print("Waiting for onboard button to be toggled...")

### STEP 4 | When the onboard button gets toggled, start reading input from the Tracking Sensor and begin moving forward
while (GPIO.input(Button) != 0):
	position,Sensors = TR.readLine()
	print(position,Sensors)
	time.sleep(0.05)
DCM.forward()

### STEP 5 | Initiate "infinit loop" 
while True:
	position,Sensors = TR.readLine()
	#print(position)
	if(Sensors[0] >900 and Sensors[1] >900 and Sensors[2] >900 and Sensors[3] >900 and Sensors[4] >900):
		DCM.setPWMAY(0);
		DCM.setPWMBY(0);
                DCM.setPWMAX(0);
		DCM.setPWMBX(0);
	else:
		# The "proportional" term should be 0 when we are on the line.
		proportional = position - 2000
		
		# Compute the derivative (change) and integral (sum) of the position.
		derivative = proportional - last_proportional
		integral += proportional
		
		# Remember the last position.
		last_proportional = proportional

		'''
		// Compute the difference between the two motor power settings,
		// m1 - m2.  If this is a positive number the robot will turn
		// to the right.  If it is a negative number, the robot will
		// turn to the left, and the magnitude of the number determines
		// the sharpness of the turn.  You can adjust the constants by which
		// the proportional, integral, and derivative terms are multiplied to
		// improve performance.
		'''
		power_difference = proportional/30  + integral/10000 + derivative*2;  

		if (power_difference > maximum):
			power_difference = maximum
		if (power_difference < - maximum):
			power_difference = - maximum
		print(position,power_difference)
		if (power_difference < 0):
			DCM.setPWMAY(maximum + power_difference)
			DCM.setPWMBY(maximum);
		else:
			DCM.setPWMAY(maximum);
			DCM.setPWMBY(maximum - power_difference)
		
