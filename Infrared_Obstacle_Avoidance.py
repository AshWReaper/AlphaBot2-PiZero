import RPi.GPIO as GPIO
import time
from DCMotors_VS import DCMotors

speed_forward = 15 # set the forward/backward speed here
speed_turn = 30 # set the turning speed here

DR = 16 # set the GPIO pin number for the right hand side sensor (Dont Change This Value!!!)
DL = 19 # set the GPIO pin number for the right hand side sensor (Dont Change This Value!!!)

FWD_STATUS = False; # set the initial forward status (false is recommended)
TEMP_STORAGE = 0; # used to count how many loop itterations occur when moving forward

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
                
                ## if the oblsicle is detected by the right-hand side sensor...
                if((DR_status == 0) and (DL_status == 1)):
                        TEMP_STORAGE = 0;
                        FWD_STATUS = False # change forward status to false
                        dcm.stop() # stop
                        dcm.left() # turn left
                        time.sleep(0.4)
                        dcm.stop() # stop
                        
                ## if the oblsicle is detected by the left-hand side sensor...
                if((DL_status == 0) and (DR_status == 1)):
                        TEMP_STORAGE = 0;
                        FWD_STATUS = False # change forward status to false
                        dcm.stop() # stop
                        dcm.right() # turn right
                        time.sleep(0.4)
                        dcm.stop() # stop
                        
                ## if the obsicle is deteted by both the left and right-hand side sensors...
                if((DR_status == 0) and (DL_status == 0)):
                        TEMP_STORAGE = 0;
                        FWD_STATUS = False # change forward status to false
                        dcm.stop() # stop
                        dcm.backward() # go backwards 
                        time.sleep(3)
                        dcm.stop() # stop
                        dcm.left() # turn left
                        time.sleep(0.8)
                        dcm.stop() # stop
                        
                ## else if the terrain is clear....
	        else:
		        # dcm.forward() # move forward

                        ## try add some extra movements in here while the bot is moving forward, but there must be no obsticals in sight...
                        FWD_STATUS = dcm.forward()
                        print(FWD_STATUS)
                        print(TEMP_STORAGE)
                        if(FWD_STATUS == True):
                                print("Moving Forward With Intent!")
                                TEMP_STORAGE+=1

                        if(FWD_STATUS == False):
                                print("doing something else with intent")

                while(TEMP_STORAGE > 3000):
                        print("FOOOO!")
                        print(DR_status)
                        DR_status = GPIO.input(DR)
                        if((DR_status == 0) or (DL_status == 0)):
                                TEMP_STORAGE = 0
                
except KeyboardInterrupt:
	GPIO.cleanup();

