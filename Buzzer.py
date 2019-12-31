#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# setup GPIO for buzzer - Should use PIN no. 4 (BCM)
Buzzer_Pin = 4

# set duration for ezbuzz
Ezbuzz_Duration = 0.8

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

GPIO.setup(Buzzer_Pin,GPIO.OUT) # set pin 4 to 'output' mode

class Buzzer:

    def __init__(self,bpin=Buzzer_Pin,bduration=Ezbuzz_Duration):
        self.BUZZER_PIN=bpin
        self.BUZZ_DURATION=bduration

    def start(self):
        GPIO.output(self.BUZZER_PIN,GPIO.HIGH)

    def stop(self):
        GPIO.output(self.BUZZER_PIN,GPIO.LOW)

    def ezbuzz(self):
        GPIO.output(self.BUZZER_PIN,GPIO.HIGH)
        time.sleep(self.BUZZ_DURATION)
        GPIO.output(self.BUZZER_PIN,GPIO.LOW)
        time.sleep(0.02)

if __name__=='__main__':
    
    bzr = Buzzer()

    try:

        print("Testing Buzzer Using 'start()' Method")
        bzr.start()
        time.sleep(0.02)
        print("Stopping Buzzer Using 'stop()' Function")
        bzr.stop()
        time.sleep(1)

        print("Testing Buzzer Using 'start()' Method")
        bzr.start()
        time.sleep(0.04)
        print("Stopping Buzzer Using 'stop()' Function")
        bzr.stop()
        time.sleep(1)

        print("Testing Buzzer Using 'start()' Method")
        bzr.start()
        time.sleep(0.06)
        print("Stopping Buzzer Using 'stop()' Function")
        bzr.stop()
        time.sleep(1)

        print("Testing Buzzer Using 'start()' Method")
        bzr.start()
        time.sleep(0.08)
        print("Stopping Buzzer Using 'stop()' Function")
        bzr.stop()
        time.sleep(1)

        print("Testing Buzzer Using 'start()' Method")
        bzr.start()
        time.sleep(0.1)
        print("Stopping Buzzer Using 'stop()' Function")
        bzr.stop()
        time.sleep(1)

        print("Testing Buzzer Using 'ezbuzz()' function")
        bzr.ezbuzz()
        time.sleep(0.2)
        
    except KeyboardInterrupt:

        bzr.stop()

    except:
        print("Problem Somewhere In The Buzzer Driver Code")
        bzr.stop()

    finally:

        print("Buzzer Testing Finished... Tying Up Loose Ends Now...")

        print("Buzzer Stopped Manually For The Last Time Using 'stop()' Function...")
        bzr.stop()

        print("Giving The System Some Time To Think About Life (Process The Stop Function)...")
        time.sleep(0.02)

        print("Cleaning Up The GPIO")
        GPIO.cleanup()

        print("All Done :) Thanks For Testing!")
        




