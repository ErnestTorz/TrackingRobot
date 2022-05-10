import RPi.GPIO as GPIO

class Robot:
    def __init__(self, DIRa,STEPa,DIRb,STEPb):
        self.DIRa=DIRa
        self.STEPa=STEPa
        self.DIRb=DIRb
        self.STEPb=STEPb
        self.frequency=250

        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(DIRa,GPIO.OUT)
        GPIO.output(DIRa,GPIO.LOW)
        GPIO.setup(STEPa,GPIO.OUT)
        self.pwmA=GPIO.PWM(STEPa,self.frequency)
        self.pwmA.start(0)

        GPIO.setup(DIRb,GPIO.OUT)
        GPIO.output(DIRb,GPIO.LOW)   
        GPIO.setup(STEPb,GPIO.OUT)
        self.pwmB=GPIO.PWM(STEPb,self.frequency)
        self.pwmB.start(0)
    
    def __del__(self):
        GPIO.cleanup()

    def stop (self):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        GPIO.output(self.DIRa,GPIO.LOW)
        GPIO.output(self.DIRb,GPIO.LOW)

    def linear_drive(self, direction, speed):
        if isinstance(speed,int) and (100 >= speed >= 0) :
            if direction=="forward" or direction=="Forward" or direction=="f" or direction=="F" :
                GPIO.output(self.DIRa,GPIO.LOW)
                GPIO.output(self.DIRb,GPIO.LOW)
                self.pwmA.ChangeDutyCycle(speed)
                self.pwmB.ChangeDutyCycle(speed)
            elif direction =="backward" or direction == "Backward" or direction=="b" or direction=="B" :
                GPIO.output(self.DIRa,GPIO.HIGH)
                GPIO.output(self.DIRb,GPIO.HIGH)
                self.pwmA.ChangeDutyCycle(speed)
                self.pwmB.ChangeDutyCycle(speed)

    def rotation_in_place(self, direction, speed):
        if isinstance(speed,int) and (100 >= speed >= 0) :
            if direction=="left" or direction=="Left" or direction=="l" or direction=="L" :
                GPIO.output(self.DIRa,GPIO.HIGH)
                GPIO.output(self.DIRb,GPIO.LOW)
                self.pwmA.ChangeDutyCycle(speed)
                self.pwmB.ChangeDutyCycle(speed)
            elif direction =="right" or direction == "Right" or direction=="r" or direction=="R" :
                GPIO.output(self.DIRa,GPIO.LOW)
                GPIO.output(self.DIRb,GPIO.HIGh)
                self.pwmA.ChangeDutyCycle(speed)
                self.pwmB.ChangeDutyCycle(speed)

#       ##Example use##
# import time
# robot=Robot(21,20,16,26,19,13)
# time.sleep(10)
# robot.linear_drive("f",30)
# time.sleep(4)
# robot.linear_drive("b",30)
# time.sleep(4)
# robot.rotation_in_place("l",40)
# time.sleep(5)
# robot.rotation_in_place("r",40)
# time.sleep(5)

    

        

    

