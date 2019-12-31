#!/usr/bin/python
import traceback,time
from PCA9685 import PCA9685 # import servo class from driver file

###

#create instance of servo driver
pwm = PCA9685(0x40, debug=True)
pwm.setPWMFreq(50) #set the frequency

#set the initial servo pulses, which "center" the servos before we begin
pwm.setServoPulse(0,1500) #horizontal?
pwm.setServoPulse(1,1500) #vertical?

try:
    print("moving pan head right")
    for i in range(1500,2500,10):
        pwm.setServoPulse(0,i)
        time.sleep(0.02)
        
    print("moving pan head up")
    for i in range(1500,2500,10):
        pwm.setServoPulse(1,i)
        time.sleep(0.02)

    print("moving pan head left")    
    for i in range(2500,500,-10):
        pwm.setServoPulse(0,i)
        time.sleep(0.02)

    print("moving pan head down")
    for i in range(2500,500,-10):
        pwm.setServoPulse(1,i)
        time.sleep(0.02)

    print("moving pan head back to center")
    for i in range(500,1500,10):
        pwm.setServoPulse(0,i)
        time.sleep(0.02)

    print("moving pan head back to center")
    for i in range(500,1500,10):
        pwm.setServoPulse(1,i)
        time.sleep(0.02)
except Exception:
    print("some issue bro!")
    traceback.print_exc()
    
finally:
    print("program finished")


"""
try:
    for i in range(500,2500,10):
        pwm.setServoPulse(0,i)
        time(0.02)

    for i in range(2500,500,-10):
        pwm.setServoPulse(0,i)
        time(0.02)
except:
    print("Some sort of issue happened...")
finally:
    print("End of program...")
"""
