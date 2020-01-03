import RPi.GPIO as GPIO
import time
from DCMotors_VS.py import DCMotors

speed_forward = 15
speed_turn = 15

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

try:
        dcm=DCMotors()
        dcm.setPWMAY(speed_forward)
        dcm.setPWMBY(speed_forward)
        dcm.setPWMAY(speed_turn)
        dcm.setPWMAX(speed_turn)
        
        while True:
		DR_status = GPIO.input(DR)
		DL_status = GPIO.input(DL)
#		print(DR_status,DL_status)
		if((DL_status == 0) or (DR_status == 0)):
			dcm.left()
			#dcm.right()
			time.sleep(0.002)
			dcm.stop()
		#	print("object")
		else:
			dcm.forward()
		#	print("forward")

except KeyboardInterrupt:
	GPIO.cleanup();

