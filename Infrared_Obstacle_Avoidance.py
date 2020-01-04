import RPi.GPIO as GPIO
import time
from DCMotors_VS import DCMotors

speed_forward = 15 # set the forward/backward speed here
speed_turn = 30 # set the turning speed here

DR = 16 # set the GPIO pin number for the right hand side sensor (Dont Change This Value!!!)
DL = 19 # set the GPIO pin number for the right hand side sensor (Dont Change This Value!!!)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

try:
        dcm=DCMotors() # create instance of our DC motors class 
        dcm.setPWMAY(speed_forward) # set the foward speed for DC Motor "A"
        dcm.setPWMBY(speed_forward) # set the foward speed for DC Motor "B"
        dcm.setPWMAX(speed_turn) # set the turning speed for DC Motor "A"
        dcm.setPWMBX(speed_turn)  # set the turning speed for DC Motor "B"
        
        while True:
		DR_status = GPIO.input(DR) # get the input from the right hand side sensor
		DL_status = GPIO.input(DL) # get the input from the left hand side sensor

                ## if either sensor picks up an obstacle....
		if((DL_status == 0) or (DR_status == 0)):
                        dcm.stop() # stop
                        dcm.backward() # go back a bit
                        time.sleep(0.1)
                        dcm.left() # turn left
                        time.sleep(0.4)
                ## else if the terrain is clear....
		else:
			dcm.forward() # move forward

except KeyboardInterrupt:
	GPIO.cleanup();

