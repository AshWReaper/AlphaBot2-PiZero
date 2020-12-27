#!/usr/bin/python
import traceback,time
from PCA9685 import PCA9685 # import servo class from driver file

###

#create instance of servo driver
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50) #set the frequency

#set the initial servo pulses, which "center" the servos before we begin
#pwm.setServoPulse(0,1500) #horizontal Axis
#pwm.setServoPulse(1,1500) #vertical Axis


## Adjust these settings to moderate the servo panning speed 
sleep_time = 0.005 # set the time between steps here
step_count = 10 # set the amount of steps for each Servo Pulse


try:

    ## START BOTH AXIS AT CENTER POINTS
    print("Centering Horizontal & Vertical Axis...")
    pwm.setServoPulse(0,1500)
    pwm.setServoPulse(1,1500)

    ## PAN CAMERA SERVO LEFT FROM CENTER POSITION
    print("Panning Left")
    for i in range(1500,2500,step_count):
        pwm.setServoPulse(0,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO BACK TO CENTER FROM LEFT POSITION
    print("Panning to center from Left")
    for i in range(2500,1500,-step_count):
        pwm.setServoPulse(0,i)
        time.sleep(sleep_time)
    
    ## PAN CAMERA SERVO RIGHT FROM CENTER POSITION
    print("Panning Right")
    for i in range(1500,500,-step_count):
        pwm.setServoPulse(0,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO SERVO UP FROM CENTER POSITION
    print("Panning Up")
    for i in range(1500,1200,-step_count):
        pwm.setServoPulse(1,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO BACK TO CENTER FROM RIGHT POSITION
    print("Panning to center from right")
    for i in range(500,1500,step_count):
        pwm.setServoPulse(0,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO SERVO UP TO TOP FROM CENTER POSITION
    print("Panning Up")
    for i in range(1200,700,-step_count):
        pwm.setServoPulse(1,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO BACK TO "UP" POSITION FROM "UP TO TOP" POSITION
    print("Panning to center from Up")
    for i in range(700,1200,step_count):
        pwm.setServoPulse(1,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO LEFT FROM CENTER POSITION
    print("Panning Left")
    for i in range(1500,2500,step_count):
        pwm.setServoPulse(0,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO BACK TO CENTER FROM UP POSITION
    print("Panning to center from Up")
    for i in range(1200,1500,step_count):
        pwm.setServoPulse(1,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO SERVO DOWN FROM CENTER POSITION
    print("Panning Down")
    for i in range(1500,2200,step_count):
        pwm.setServoPulse(1,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO BACK TO CENTER FROM LEFT POSITION
    print("Panning to center from Left")
    for i in range(2500,1500,-step_count):
        pwm.setServoPulse(0,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO RIGHT FROM CENTER POSITION
    print("Panning Right")
    for i in range(1500,500,-step_count):
        pwm.setServoPulse(0,i)
        time.sleep(sleep_time)
        
    ## PAN CAMERA SERVO BACK TO CENTER FROM DOWN POSITION
    print("Panning to center from Down")
    for i in range(2200,1500,-step_count):
        pwm.setServoPulse(1,i)
        time.sleep(sleep_time)

    ## PAN CAMERA SERVO BACK TO CENTER FROM RIGHT POSITION
    print("Panning to center from right")
    for i in range(500,1500,step_count):
        pwm.setServoPulse(0,i)
        time.sleep(sleep_time)

except Exception:
    print("There seems to be an issue with the program...")
    traceback.print_exc()
    
finally:
    print("program finished")
