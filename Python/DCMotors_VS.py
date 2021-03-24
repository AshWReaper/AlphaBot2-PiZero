#
# CREDIT: This code was taken from the Waveshare AlphaBot2 example code (AlphaBot2.py)
# URL: ??
#

import RPi.GPIO as GPIO # import the Raspberry Pi GPIO library
import time # import time library

class DCMotors(object):
	
	def __init__(self,ain1=12,ain2=13,ena=6,bin1=20,bin2=21,enb=26):
		self.AIN1 = ain1
		self.AIN2 = ain2
		self.BIN1 = bin1
		self.BIN2 = bin2
		self.ENA = ena
		self.ENB = enb
                ## Set initial 'Pulse Width Modulation' values | Affects the speed of our DC Motors
                self.PAY = 50 # side A on the Y axis (Forward & Backward Movements)
		self.PBY = 50 # side B on the Y axis (Forward & Backward Movements)
                self.PAX = 15 # side A on the X axis (Left & Right Turning)
                self.PBX = 15 # side B on the X axis (Left & Right Turning)

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.AIN1,GPIO.OUT)
		GPIO.setup(self.AIN2,GPIO.OUT)
		GPIO.setup(self.BIN1,GPIO.OUT)
		GPIO.setup(self.BIN2,GPIO.OUT)
		GPIO.setup(self.ENA,GPIO.OUT)
		GPIO.setup(self.ENB,GPIO.OUT)
		self.PWMA = GPIO.PWM(self.ENA,500)
		self.PWMB = GPIO.PWM(self.ENB,500)
		self.PWMA.start(self.PAY)
		self.PWMB.start(self.PBY)
		self.stop()

	def forward(self):
		self.PWMA.ChangeDutyCycle(self.PAY)
		self.PWMB.ChangeDutyCycle(self.PBY)
		GPIO.output(self.AIN1,GPIO.LOW)
		GPIO.output(self.AIN2,GPIO.HIGH)
		GPIO.output(self.BIN1,GPIO.LOW)
		GPIO.output(self.BIN2,GPIO.HIGH)
                return True

	def stop(self):
		self.PWMA.ChangeDutyCycle(0)
		self.PWMB.ChangeDutyCycle(0)
		GPIO.output(self.AIN1,GPIO.LOW)
		GPIO.output(self.AIN2,GPIO.LOW)
		GPIO.output(self.BIN1,GPIO.LOW)
		GPIO.output(self.BIN2,GPIO.LOW)

	def backward(self):
		self.PWMA.ChangeDutyCycle(self.PAY)
		self.PWMB.ChangeDutyCycle(self.PBY)
		GPIO.output(self.AIN1,GPIO.HIGH)
		GPIO.output(self.AIN2,GPIO.LOW)
		GPIO.output(self.BIN1,GPIO.HIGH)
		GPIO.output(self.BIN2,GPIO.LOW)

		
	def left(self):
		self.PWMA.ChangeDutyCycle(self.PAX)
		self.PWMB.ChangeDutyCycle(self.PBX)
		GPIO.output(self.AIN1,GPIO.HIGH)
		GPIO.output(self.AIN2,GPIO.LOW)
		GPIO.output(self.BIN1,GPIO.LOW)
		GPIO.output(self.BIN2,GPIO.HIGH)


	def right(self):
		self.PWMA.ChangeDutyCycle(self.PAX)
		self.PWMB.ChangeDutyCycle(self.PBX)
		GPIO.output(self.AIN1,GPIO.LOW)
		GPIO.output(self.AIN2,GPIO.HIGH)
		GPIO.output(self.BIN1,GPIO.HIGH)
		GPIO.output(self.BIN2,GPIO.LOW)

        ## Set PWM for Motor A on the Y axis (Forward/Backard)
	def setPWMAY(self,value):
		self.PAY = value
		self.PWMA.ChangeDutyCycle(self.PAY)

        ## Set PWM for Motor B on the Y axis (Forward/Backard)        
	def setPWMBY(self,value):
		self.PBY = value
		self.PWMB.ChangeDutyCycle(self.PBY)

        ## Set PWM for Motor A on the X axis (Left/Right)
        def setPWMAX(self,value):
		self.PAX = value
		self.PWMA.ChangeDutyCycle(self.PAX)

        ## Set PWM for Motor B on the X axis (Left/Right)       
	def setPWMBX(self,value):
		self.PBX = value
		self.PWMB.ChangeDutyCycle(self.PBX)
		
	def setMotor(self, left, right):
		if((right >= 0) and (right <= 100)):
			GPIO.output(self.AIN1,GPIO.HIGH)
			GPIO.output(self.AIN2,GPIO.LOW)
			self.PWMA.ChangeDutyCycle(right)
		elif((right < 0) and (right >= -100)):
			GPIO.output(self.AIN1,GPIO.LOW)
			GPIO.output(self.AIN2,GPIO.HIGH)
			self.PWMA.ChangeDutyCycle(0 - right)
		if((left >= 0) and (left <= 100)):
			GPIO.output(self.BIN1,GPIO.HIGH)
			GPIO.output(self.BIN2,GPIO.LOW)
			self.PWMB.ChangeDutyCycle(left)
		elif((left < 0) and (left >= -100)):
			GPIO.output(self.BIN1,GPIO.LOW)
			GPIO.output(self.BIN2,GPIO.HIGH)
			self.PWMB.ChangeDutyCycle(0 - left)

if __name__=='__main__':

        # set time limits for movements here
        Forward_t = 1    # forwards
        Backward_t = 1   # backards
        Left_t = 0.5     # left turn
        Right_t = 0.5    # right turn
        Break__s_t = 0.2 # break (short)
        Break__l_t = 0.2 # break (long)
        Speed_Slow=10
        Speed_Med=25
        Speed_Fast=50
        
	dcm = DCMotors()
	
	try:

                print("Turning Left...")
                dcm.setPWMAX(Speed_Slow)
                dcm.setPWMBX(Speed_Slow)
                dcm.left()
                time.sleep(Left_t)

                print("Stopping...")
                dcm.stop()
                time.sleep(Break__s_t)

                print("Turning Right...")
                dcm.right()
                time.sleep(Right_t)

                print("Stopping...")
                dcm.stop()
                time.sleep(Break__s_t)

                print("Moving Forward")
                dcm.setPWMAY(Speed_Fast)
                dcm.setPWMBY(Speed_Fast)
                dcm.forward()
		time.sleep(Forward_t)

                print("Stopping...")
                dcm.stop()
                time.sleep(Break__s_t)

                print("Moving Backwards")
                dcm.setPWMAY(Speed_Med)
                dcm.setPWMBY(Speed_Med)
                dcm.backward()
                time.sleep(Backward_t)

                print("Stopping...")
                dcm.stop()
                time.sleep(Break__s_t)

                
                print("Cleaning up GPIO's")
                GPIO.cleanup() # clean up GPIO's after use...
                
	except KeyboardInterrupt:
		GPIO.cleanup()
