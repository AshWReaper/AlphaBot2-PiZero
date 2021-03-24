#!/usr/bin/python

######################################
# Infrared Obstacle Avoidance Sensor #
######################################

# import necessary libraries
import RPi.GPIO as GPIO
import time

# Set pin numbers (Should be 16 & 19 [BCM])
Right_Sensor=16
Left_Sensor=19

# Set mode for GPIO (Should be BCM)
GPIO.setmode(GPIO.BCM)

# Set warnings (True/False)
GPIO.setwarnings(True)

# Setup the GPIO pins
GPIO.setup(Right_Sensor,GPIO.IN,GPIO.PUD_UP) # Right sensor, set to input
GPIO.setup(Left_Sensor,GPIO.IN,GPIO.PUD_UP) # Left sensor, set to input

class IOAS():

    def __init__(self,rsensor=Right_Sensor,lsensor=Left_Sensor):
        self.RIGHT_SENSOR=rsensor
        self.LEFT_SENSOR=lsensor

    def read_right_sensor_value(self):
        Current_Right_Sensor_Value=GPIO.input(self.RIGHT_SENSOR)
        return Current_Right_Sensor_Value
    
    def read_left_sensor_value(self):
        Current_Left_Sensor_Value=GPIO.input(self.LEFT_SENSOR)
        return Current_Left_Sensor_Value

    def read_both_sensor_values(self):
        Current_Right_Sensor_Value=GPIO.input(self.RIGHT_SENSOR)
        Current_Left_Sensor_Value=GPIO.input(self.LEFT_SENSOR)
        Both_Values=[Current_Right_Sensor_Value,Current_Left_Sensor_Value]
        return Both_Values
    
if __name__ == '__main__':

    try:
        print("Starting Test Sequence For Infrared Obstacle Avoidance Sensors (IOAS)")
        print("NOTE: 6 'tests' will be run in total, which should take around 3 seconds to complete...")
        
        sensors=IOAS()

        print("Independent Testing Of Sensors...")
        for i in range(1,4,1):
            print("Test ",i)
            test_value_right_sensor=sensors.read_right_sensor_value()
            test_value_left_sensor=sensors.read_left_sensor_value()
            print("Right Sensor Value: ",test_value_right_sensor,"Left Sensor Value: ",test_value_left_sensor)
            time.sleep(0.5)
    
        print("Now The Duel Test...")
        for i in range(1,4,1):
            print("Test ",i)
            test_value_both=sensors.read_both_sensor_values()
            print("Values For Both Sensors [R/L]: ",test_value_both)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Process Interrupted By User...")

    except:
        print("Something Bad Happened Boss... (o_0)")

    finally:
        print("Program Finished... Tying Up Loose Ends Now...")
        GPIO.cleanup()
