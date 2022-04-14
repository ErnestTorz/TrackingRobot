from time import sleep

import RPi.GPIO as GPIO
from numpy import int32

in1 = 20 #in1
in2 = 16 #in2
ena = 21 #ena

in3 = 26 #in3
in4 = 19 #in4
enb = 13 #enb

frequency=250

temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
pwmA=GPIO.PWM(ena,frequency)

pwmA.start(25)

GPIO.setmode(GPIO.BCM)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
pwmB=GPIO.PWM(enb,frequency)

pwmB.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

while(1):
    
    x=input()
    
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in4,GPIO.HIGH)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in4,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         GPIO.output(in3,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in4,GPIO.HIGH)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        pwmA.ChangeDutyCycle(25)
        pwmB.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        pwmA.ChangeDutyCycle(50)
        pwmB.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        pwmA.ChangeDutyCycle(75)
        pwmB.ChangeDutyCycle(75)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
