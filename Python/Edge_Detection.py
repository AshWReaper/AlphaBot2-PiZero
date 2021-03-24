#!/usr/bin/python

import traceback, time
from DCMotors_VS import DCMotors
from TRSensors import TRSensor

try:
    dcm=DCMotors()
    trs=TRSensor()
    edv=100 # edge detection value

    speed=2
    dcm.setPWMAY(speed) # slow motor A down (forward/backward)
    dcm.setPWMBY(speed) # slow motor B down (forward/backward)
    dcm.setPWMAX(speed) # slow motor A down (turning)
    dcm.setPWMBX(speed) # slow motor B down (turning)
            
    while True:

        # store the TRSensor values (an array)
        trs_va=trs.AnalogRead()

        if trs_va[0] < edv or trs_va[1] < edv or trs_va[2] < edv or trs_va[3] < edv or trs_va[4] < edv:
            ## code for what happens when an edge is detected
            print("edge detected")
            
            dcm.stop() # stop both DC motors

            dcm.backward()
            #time.sleep(0.2)
            time.sleep(2)

            dcm.stop()
            time.sleep(0.2)

            #dcm.left()
            #time.sleep(0.2)

        else:
            ## foo
            print("all seems safe... for now...")
            dcm.forward()

except KeyboardInterrupt:
    print("ended by user")

except:
    print("Something went wrong here...")
    print traceback.print_exc()
    
