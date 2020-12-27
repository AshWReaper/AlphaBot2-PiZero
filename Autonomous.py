import RPi.GPIO as GPIO
import time

from DCMotors_VS import DCMotors # import DC Motor class from driver file

from PCA9685 import PCA9685 # import servo class from driver file

speed_forward = 15 # set the forward/backward speed here
speed_turn = 30 # set the turning speed here

## Adjust these settings to moderate the servo panning speed 
SERVO_SLEEP_TIME = 0.005 # set the time between steps here
SERVO_STEP_COUNT = 10 # set the amount of steps for each Servo Pulse


DR = 16 # set the GPIO pin number for the right hand side sensor (Dont Change This Value!!!)
DL = 19 # set the GPIO pin number for the right hand side sensor (Dont Change This Value!!!)

FWD_STATUS = False; # set the initial forward status (false is recommended)
DISTANCE_TRAVELED = 0; # used to count how many loop itterations occur when moving forward

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

try:
        ## setup the DC Motors
        dcm=DCMotors() # create instance of our DC motors class 
        dcm.setPWMAY(speed_forward) # set the foward speed for DC Motor "A"
        dcm.setPWMBY(speed_forward) # set the foward speed for DC Motor "B"
        dcm.setPWMAX(speed_turn) # set the turning speed for DC Motor "A"
        dcm.setPWMBX(speed_turn)  # set the turning speed for DC Motor "B"

        ## setup the Servo Motors
        pwm = PCA9685(0x40, debug=False) #create instance of servo driver
        pwm.setPWMFreq(50) #set the frequency
        #set the initial servo pulses, which "center" the servos before we begin
        pwm.setServoPulse(0,1500) #horizontal Axis
        pwm.setServoPulse(1,1500) #vertical Axis
        
        while True:
		DR_status = GPIO.input(DR) # get the input from the right hand side sensor
		DL_status = GPIO.input(DL) # get the input from the left hand side sensor
                
                ## if the oblsicle is detected by the right-hand side sensor...
                if((DR_status == 0) and (DL_status == 1)):
                        DISTANCE_TRAVELED = 0;
                        FWD_STATUS = False # change forward status to false
                        dcm.stop() # stop
                        dcm.left() # turn left
                        time.sleep(0.4)
                        dcm.stop() # stop
                        
                ## if the oblsicle is detected by the left-hand side sensor...
                elif((DL_status == 0) and (DR_status == 1)):
                        DISTANCE_TRAVELED = 0;
                        FWD_STATUS = False # change forward status to false
                        dcm.stop() # stop
                        dcm.right() # turn right
                        time.sleep(0.4)
                        dcm.stop() # stop
                        
                ## if the obsicle is deteted by both the left and right-hand side sensors...
                elif((DR_status == 0) and (DL_status == 0)):
                        DISTANCE_TRAVELED = 0;
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
                        print(DISTANCE_TRAVELED)
                        if(FWD_STATUS == True):
                                print("Moving Forward With Intent!")
                                DISTANCE_TRAVELED+=1

                        else:
                                print("doing something else with intent") ## wierdly... this never seemes to trigger... try figure out why?

                        ## Trigger every time the bot goes a certain distance forward with no obstruciotns
                        if((DISTANCE_TRAVELED % 3000) == 0):
                                dcm.stop()
                                time.sleep(3)
                                dcm.left()
                                time.sleep(0.4)
                                dcm.stop()
                                time.sleep(1)
                                dcm.right()
                                time.sleep(0.8)
                                dcm.stop()
                                time.sleep(1)

                        elif((DISTANCE_TRAVELED % 5000) == 0):
                                dcm.stop()

                                try:
                                        ## START BOTH AXIS AT CENTER POINTS
                                        print("Centering Horizontal & Vertical Axis...")
                                        pwm.setServoPulse(0,1500)
                                        pwm.setServoPulse(1,1500)

                                        ## PAN CAMERA SERVO LEFT FROM CENTER POSITION
                                        print("Panning Left")
                                        for i in range(1500,2500,SERVO_STEP_COUNT):
                                                pwm.setServoPulse(0,i)
                                                time.sleep(SERVO_SLEEP_TIME)
                                                
                                        ## PAN CAMERA SERVO BACK TO CENTER FROM LEFT POSITION
                                        print("Panning to center from Left")
                                        for i in range(2500,1500,-SERVO_STEP_COUNT):
                                                pwm.setServoPulse(0,i)
                                                time.sleep(SERVO_SLEEP_TIME)
                                                
                                        ## PAN CAMERA SERVO RIGHT FROM CENTER POSITION
                                        print("Panning Right")
                                        for i in range(1500,500,-SERVO_STEP_COUNT):
                                                pwm.setServoPulse(0,i)
                                                time.sleep(SERVO_SLEEP_TIME)
                                                
                                        ## PAN CAMERA SERVO SERVO UP FROM CENTER POSITION
                                        print("Panning Up")
                                        for i in range(1500,1200,-SERVO_STEP_COUNT):
                                                pwm.setServoPulse(1,i)
                                                time.sleep(SERVO_SLEEP_TIME)
                                        
                                        ## PAN CAMERA SERVO BACK TO CENTER FROM RIGHT POSITION
                                        print("Panning to center from right")
                                        for i in range(500,1500,SERVO_STEP_COUNT):
                                                pwm.setServoPulse(0,i)
                                                time.sleep(SERVO_SLEEP_TIME)

                                        ## PAN CAMERA SERVO SERVO UP TO TOP FROM CENTER POSITION
                                        print("Panning Up")
                                        for i in range(1200,700,-SERVO_STEP_COUNT):
                                                pwm.setServoPulse(1,i)
                                                time.sleep(SERVO_SLEEP_TIME)

                                        ## PAN CAMERA SERVO BACK TO "UP" POSITION FROM "UP TO TOP" POSITION
                                        print("Panning to center from Up")
                                        for i in range(700,1200,SERVO_STEP_COUNT):
                                                pwm.setServoPulse(1,i)
                                                time.sleep(SERVO_SLEEP_TIME)

                                        ## PAN CAMERA SERVO LEFT FROM CENTER POSITION
                                        print("Panning Left")
                                        for i in range(1500,2500,SERVO_STEP_COUNT):
                                                pwm.setServoPulse(0,i)
                                                time.sleep(SERVO_SLEEP_TIME)

                                        ## PAN CAMERA SERVO BACK TO CENTER FROM UP POSITION
                                        print("Panning to center from Up")
                                        for i in range(1200,1500,SERVO_STEP_COUNT):
                                                pwm.setServoPulse(1,i)
                                                time.sleep(SERVO_SLEEP_TIME)

                                        ## PAN CAMERA SERVO SERVO DOWN FROM CENTER POSITION
                                        print("Panning Down")
                                        for i in range(1500,2200,SERVO_STEP_COUNT):
                                                pwm.setServoPulse(1,i)
                                                time.sleep(SERVO_SLEEP_TIME)

                                        ## PAN CAMERA SERVO BACK TO CENTER FROM LEFT POSITION
                                        print("Panning to center from Left")
                                        for i in range(2500,1500,-SERVO_STEP_COUNT):
                                                pwm.setServoPulse(0,i)
                                                time.sleep(SERVO_SLEEP_TIME)

                                        ## PAN CAMERA SERVO RIGHT FROM CENTER POSITION
                                        print("Panning Right")
                                        for i in range(1500,500,-SERVO_STEP_COUNT):
                                                pwm.setServoPulse(0,i)
                                                time.sleep(SERVO_SLEEP_TIME)
                                        
                                        ## PAN CAMERA SERVO BACK TO CENTER FROM DOWN POSITION
                                        print("Panning to center from Down")
                                        for i in range(2200,1500,-SERVO_STEP_COUNT):
                                                pwm.setServoPulse(1,i)
                                                time.sleep(SERVO_SLEEP_TIME)

                                        ## PAN CAMERA SERVO BACK TO CENTER FROM RIGHT POSITION
                                        print("Panning to center from right")
                                        for i in range(500,1500,SERVO_STEP_COUNT):
                                                pwm.setServoPulse(0,i)
                                                time.sleep(SERVO_SLEEP_TIME)

                                except Exception:
                                        print("There seems to be an issue with the program...")
                                        traceback.print_exc()
                                
                                finally:
                                        print("program finished")
                                
                
except KeyboardInterrupt:
	GPIO.cleanup();
