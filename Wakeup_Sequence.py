#!/usr/bin/python
import traceback,time
from PCA9685 import PCA9685 # import servo class from driver file

###

#create instance of servo driver
pwm = PCA9685(0x40, debug=True)
pwm.setPWMFreq(50) #set the frequency

#set the initial servo pulses, which "center" the servos before we begin
pwm.setServoPulse(0,1500) #horizontal
pwm.setServoPulse(1,1500) #vertical

try:
    #set the initial servo pulses, which should be close enough to the point where the bot went to sleep
    pwm.setServoPulse(0,1500) #horizontal
    pwm.setServoPulse(1,700) #vertical


    print("moving pan head up")
    for i in range(2000,1500,-5):
        pwm.setServoPulse(1,i)
        time.sleep(0.02)
    
    print("moving pan head right")
    for i in range(1500,1600,5):
        pwm.setServoPulse(0,i)
        time.sleep(0.02)

    print("moving pan head left")    
    for i in range(1600,1400,-5):
        pwm.setServoPulse(0,i)
        time.sleep(0.02)
        
    print("moving pan head right (back to center)")
    for i in range(1400,1500,5):
        pwm.setServoPulse(0,i)
        time.sleep(0.02)
        
except Exception:
    print("some issue bro!")
    traceback.print_exc()
    
finally:
    print("program finished")
