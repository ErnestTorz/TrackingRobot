from distutils.log import error
from itertools import count
import time
from threading import Thread
from turtle import right
import RPi.GPIO as GPIO
import math
import Sensor_vl6180x

STOP=0
FORWARD=1
BACKWARD=2
L_ROTATION=3
R_ROTATION=4
LEFT=5
RIGHT=6

class Robot:
    def __init__(self, A_ena, A_in1, A_in2, A_in3, A_in4, A_enb, B_ena, B_in1, B_in2, B_in3, B_in4, B_enb):
        self.direction=STOP

        self.counter_track=0

        self.A_ena = A_ena
        self.A_in1 = A_in1
        self.A_in2 = A_in2
        self.A_in3 = A_in3
        self.A_in4 = A_in4
        self.A_enb = A_enb
       
        self.B_ena = B_ena
        self.B_in1 = B_in1
        self.B_in2 = B_in2
        self.B_in3 = B_in3
        self.B_in4 = B_in4
        self.B_enb = B_enb
       
        self.frequency = 500
        self.pom_thread = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(A_in1, GPIO.OUT)
        GPIO.setup(A_in2, GPIO.OUT)
        GPIO.setup(A_ena, GPIO.OUT)
        GPIO.output(A_in1, GPIO.LOW)
        GPIO.output(A_in2, GPIO.LOW)
        self.A_pwmA = GPIO.PWM(A_ena, self.frequency)
        self.A_pwmA.start(0)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(A_in3, GPIO.OUT)
        GPIO.setup(A_in4, GPIO.OUT)
        GPIO.setup(A_enb, GPIO.OUT)
        GPIO.output(A_in3, GPIO.LOW)
        GPIO.output(A_in4, GPIO.LOW)
        self.A_pwmB = GPIO.PWM(A_enb, self.frequency)
        self.A_pwmB.start(0)
        ######################################################
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(B_in1, GPIO.OUT)
        GPIO.setup(B_in2, GPIO.OUT)
        GPIO.setup(B_ena, GPIO.OUT)
        GPIO.output(B_in1, GPIO.LOW)
        GPIO.output(B_in2, GPIO.LOW)
        self.B_pwmA = GPIO.PWM(B_ena, self.frequency)
        self.B_pwmA.start(0)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(B_in3, GPIO.OUT)
        GPIO.setup(B_in4, GPIO.OUT)
        GPIO.setup(B_enb, GPIO.OUT)
        GPIO.output(B_in3, GPIO.LOW)
        GPIO.output(B_in4, GPIO.LOW)
        self.B_pwmB = GPIO.PWM(B_enb, self.frequency)
        self.B_pwmB.start(0)


        self.Sensors=Sensor_vl6180x.Range_Sensors(1,6,5,12)
        self.readings= self.Sensors.reading()
    
    def __del__(self):
        GPIO.cleanup()
    
    def run(self, frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax):

        if self.pom_thread == 0:
            if(self.counter_track>10):
                self.readings= self.Sensors.reading()
                self.counter_track=0
            else:
                self.counter_track+=1
            self.thread = Thread(target=self.robot_controler, args=(frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax)).start()
            self.pom_thread = 1
        if ((Thread)(self.thread)).is_alive() == False:
            if(self.counter_track>10):
                self.readings= self.Sensors.reading()
                self.counter_track=0
            else:
                self.counter_track+=1
            self.thread = Thread(target=self.robot_controler, args=(frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax)).start()
    
    def  obstacle_detection(self):
        self.obstacle_flaga=False
     
        # if(self.direction==FORWARD):
        #     if(readings[0]>10 and readings[0]<=150 and (readings[1]<10 or readings[1]>150)):
        #         start=time.time()
        #         self.stop()
        #         while(start-time.time()<3  and readings[0]>10 and readings[0]<150):
        #             readings= self.Sensors.reading()
        #         while (readings[0]>10 and readings[0]<150  and (readings[1]<10 or readings[1]>150 )):
        #             self.linear_drive("r",90,0,0)
        #             readings= self.Sensors.reading()
        #         self.stop()

        # if(self.direction==FORWARD):
        #     if(readings[1]>10 and readings[1]<=150 and (readings[0]<10 or readings[0]>150)):
        #         start=time.time()
        #         self.stop()
        #         while(start-time.time()<3 and readings[1]>10 and readings[1]<150  ):
        #             readings= self.Sensors.reading()
        #         while (readings[1]>10 and readings[1]<150 and (readings[0]<10 or readings[0]>150)):
        #             self.linear_drive("l",90,0,0)
        #             readings= self.Sensors.reading()
        #         self.stop()

        # if(self.direction==BACKWARD):
        #     if(readings[2]>10 and readings[2]<=150 and readings[3]>150):
        #         start=time.time()
        #         self.stop()
        #         while(start-time.time()<5 and readings[2]<150  ):
        #             readings= self.Sensors.reading()
        #         while (readings[2]<150 and readings[3]>150):
        #             self.linear_drive("r",90,0,0)
        #             readings= self.Sensors.reading()
        #         self.stop()
        
        # if(self.direction==BACKWARD):
        #     if(readings[3]>10 and readings[3]<=150 and readings[2]>150):
        #         start=time.time()
        #         self.stop()
        #         while(start-time.time()<5 and readings[3]<150  ):
        #             readings= self.Sensors.reading()
        #         while (readings[3]<150 and readings[2]>150):
        #             self.linear_drive("l",90,0,0)
        #             readings= self.Sensors.reading()
        #         self.stop()
        
        if(self.direction==BACKWARD):
            if(self.readings[2]>10 and self.readings[2]<=150 and self.readings[3]>10 and self.readings[3]<=150):
                self.stop()
                print("stop")
                self.obstacle_flaga=True
                
            
        
                
                
    def stop (self):
        self.A_pwmA.ChangeDutyCycle(0)
        self.A_pwmB.ChangeDutyCycle(0)
        GPIO.output(self.A_in1, GPIO.LOW)
        GPIO.output(self.A_in2, GPIO.LOW)
        GPIO.output(self.A_in3, GPIO.LOW)
        GPIO.output(self.A_in4, GPIO.LOW)

        self.B_pwmA.ChangeDutyCycle(0)
        self.B_pwmB.ChangeDutyCycle(0)
        GPIO.output(self.B_in1, GPIO.LOW)
        GPIO.output(self.B_in2, GPIO.LOW)
        GPIO.output(self.B_in3, GPIO.LOW)
        GPIO.output(self.B_in4, GPIO.LOW)

    def linear_drive(self, direction, speed, error, Kp):
        minspeed = 48.00
        maxspeed = 100
        if isinstance(speed, int) and (100 >= speed >= 0):
            if direction == "forward" or direction == "Forward" or direction == "f" or direction == "F":
                self.direction=FORWARD
                # self.obstacle_detection()
                GPIO.output(self.A_in2, GPIO.LOW)
                GPIO.output(self.A_in3, GPIO.LOW)
                GPIO.output(self.A_in1, GPIO.HIGH)
                GPIO.output(self.A_in4, GPIO.HIGH)

                GPIO.output(self.B_in1, GPIO.LOW)
                GPIO.output(self.B_in4, GPIO.LOW)
                GPIO.output(self.B_in2, GPIO.HIGH)
                GPIO.output(self.B_in3, GPIO.HIGH)

                if (speed + (error * Kp)) >= maxspeed:
                    self.B_pwmA.ChangeDutyCycle(maxspeed)
                    self.B_pwmB.ChangeDutyCycle(maxspeed)
                elif(speed + (error * Kp)) <= minspeed:
                    self.B_pwmA.ChangeDutyCycle(minspeed)
                    self.B_pwmB.ChangeDutyCycle(minspeed)
                else:
                    self.B_pwmA.ChangeDutyCycle(speed + (error * Kp))
                    self.B_pwmB.ChangeDutyCycle(speed + (error * Kp))

                if(speed - (error * Kp)) > maxspeed:
                    self.A_pwmA.ChangeDutyCycle(maxspeed)
                    self.A_pwmB.ChangeDutyCycle(maxspeed)
                elif(speed - (error * Kp)) < minspeed:
                    self.A_pwmA.ChangeDutyCycle(minspeed)
                    self.A_pwmB.ChangeDutyCycle(minspeed)
                else:
                    self.A_pwmA.ChangeDutyCycle(speed - (error * Kp))
                    self.A_pwmB.ChangeDutyCycle(speed - (error * Kp))

            elif direction == "backward" or direction == "Backward" or direction == "b" or direction == "B":
                self.direction=BACKWARD
                self.obstacle_detection()
                if(self.obstacle_flaga==False):
                    GPIO.output(self.A_in1, GPIO.LOW)
                    GPIO.output(self.A_in4, GPIO.LOW)
                    GPIO.output(self.A_in2, GPIO.HIGH)
                    GPIO.output(self.A_in3, GPIO.HIGH)

                    GPIO.output(self.B_in2, GPIO.LOW)
                    GPIO.output(self.B_in3, GPIO.LOW)
                    GPIO.output(self.B_in1, GPIO.HIGH)
                    GPIO.output(self.B_in4, GPIO.HIGH)

                    if(speed - (error * Kp)) > maxspeed:
                        self.B_pwmA.ChangeDutyCycle(maxspeed)
                        self.B_pwmB.ChangeDutyCycle(maxspeed)
                    elif(speed - (error * Kp)) < minspeed:
                        self.B_pwmA.ChangeDutyCycle(minspeed)
                        self.B_pwmB.ChangeDutyCycle(minspeed)
                    else:
                        self.B_pwmA.ChangeDutyCycle(speed - (error * Kp))
                        self.B_pwmB.ChangeDutyCycle(speed - (error * Kp))

                    if(speed + (error * Kp)) > maxspeed:
                        self.A_pwmA.ChangeDutyCycle(maxspeed)
                        self.A_pwmB.ChangeDutyCycle(maxspeed)
                    elif(speed + (error * Kp)) < minspeed:
                        self.A_pwmA.ChangeDutyCycle(minspeed)
                        self.A_pwmB.ChangeDutyCycle(minspeed)
                    else:
                        self.A_pwmA.ChangeDutyCycle(speed + (error * Kp))
                        self.A_pwmB.ChangeDutyCycle(speed + (error * Kp))
            
            elif direction == "right" or direction == "Right" or direction == "r" or direction == "R":
                self.direction=RIGHT
                GPIO.output(self.A_in1, GPIO.LOW)
                GPIO.output(self.A_in3, GPIO.LOW)
                GPIO.output(self.A_in2, GPIO.HIGH)
                GPIO.output(self.A_in4, GPIO.HIGH)
                self.A_pwmA.ChangeDutyCycle(speed)
                self.A_pwmB.ChangeDutyCycle(speed)

                GPIO.output(self.B_in2, GPIO.LOW)
                GPIO.output(self.B_in4, GPIO.LOW)
                GPIO.output(self.B_in1, GPIO.HIGH)
                GPIO.output(self.B_in3, GPIO.HIGH)
                self.B_pwmA.ChangeDutyCycle(speed)
                self.B_pwmB.ChangeDutyCycle(speed)

            elif direction == "left" or direction == "Left" or direction == "l" or direction == "L":
                self.direction=LEFT
                GPIO.output(self.A_in2, GPIO.LOW)
                GPIO.output(self.A_in4, GPIO.LOW)
                GPIO.output(self.A_in1, GPIO.HIGH)
                GPIO.output(self.A_in3, GPIO.HIGH)
                self.A_pwmA.ChangeDutyCycle(speed)
                self.A_pwmB.ChangeDutyCycle(speed)

                GPIO.output(self.B_in1, GPIO.LOW)
                GPIO.output(self.B_in3, GPIO.LOW)
                GPIO.output(self.B_in2, GPIO.HIGH)
                GPIO.output(self.B_in4, GPIO.HIGH)
                self.B_pwmA.ChangeDutyCycle(speed)
                self.B_pwmB.ChangeDutyCycle(speed)


    def rotation_in_place(self, direction, speed):
        if isinstance(speed, int) and (100 >= speed >= 0):
            if direction == "left" or direction == "Left" or direction == "l" or direction == "L":
                self.direction=L_ROTATION
                GPIO.output(self.A_in1, GPIO.LOW)
                GPIO.output(self.A_in4, GPIO.LOW)
                GPIO.output(self.A_in2, GPIO.HIGH)
                GPIO.output(self.A_in3, GPIO.HIGH)
                self.A_pwmA.ChangeDutyCycle(speed)
                self.A_pwmB.ChangeDutyCycle(speed)

                GPIO.output(self.B_in1, GPIO.LOW)
                GPIO.output(self.B_in4, GPIO.LOW)
                GPIO.output(self.B_in2, GPIO.HIGH)
                GPIO.output(self.B_in3, GPIO.HIGH)
                self.B_pwmA.ChangeDutyCycle(speed)
                self.B_pwmB.ChangeDutyCycle(speed)

            elif direction == "right" or direction == "Right" or direction == "r" or direction == "R":
                self.direction=R_ROTATION
                GPIO.output(self.A_in2, GPIO.LOW)
                GPIO.output(self.A_in3, GPIO.LOW)
                GPIO.output(self.A_in1, GPIO.HIGH)
                GPIO.output(self.A_in4, GPIO.HIGH)
                self.A_pwmA.ChangeDutyCycle(speed)
                self.A_pwmB.ChangeDutyCycle(speed)

                GPIO.output(self.B_in2, GPIO.LOW)
                GPIO.output(self.B_in3, GPIO.LOW)
                GPIO.output(self.B_in1, GPIO.HIGH)
                GPIO.output(self.B_in4, GPIO.HIGH)
                self.B_pwmA.ChangeDutyCycle(speed)
                self.B_pwmB.ChangeDutyCycle(speed)
    
    def robot_controler(self, frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax):
        ##LINIOWA JAZDA##
        Kplf = 50
        Kplb = 50
        KplRide=35
        BaseSpeedL=52
        MAXSPEEDL=85

        ##ROTACJA###
        Kpr= 40
        BaseSpeedR=50
        MAXSPEEDR=80
        
        if object_x_center >= (frame_x_size / 5) * 3: 
            errorX=(object_x_center-((frame_x_size / 5) * 3))/(frame_x_size-((frame_x_size / 5) * 3))
            if(errorX*Kpr+BaseSpeedR>MAXSPEEDR):
                self.rotation_in_place('r',MAXSPEEDR)
            else:
                self.rotation_in_place('r',int(math.floor(errorX*Kpr+BaseSpeedR)))

        elif object_x_center <= (frame_x_size / 5) * 2:
            errorX=(((frame_x_size / 5) * 2)-object_x_center)/((frame_x_size / 5) * 2)
            if(errorX*Kpr+BaseSpeedR>MAXSPEEDR):
                self.rotation_in_place('l',MAXSPEEDR)
            else:
                self.rotation_in_place('l',int(math.floor(errorX*Kpr+BaseSpeedR)))

        elif ((float)(ymax - ymin)) / frame_y_size > 0.95:
            errorX = ((frame_x_size / 2) - object_x_center) / (frame_x_size / 2)
            errorY=((((float)(ymax - ymin)) / frame_y_size)-0.95)/(1-0.95)
            if(errorY*KplRide+BaseSpeedL>MAXSPEEDL):
                self.linear_drive("b", MAXSPEEDL, errorX, Kplb)
            else:
                self.linear_drive("b",int(math.floor(errorY*KplRide+BaseSpeedL)), errorX, Kplb)

        elif ((float)(ymax - ymin)) / frame_y_size < 0.85:
            errorX = ((frame_x_size / 2) - object_x_center) / (frame_x_size / 2)
            errorY=(85-(((float)(ymax - ymin)) / frame_y_size))/(85)
            if(errorY*KplRide+BaseSpeedL>MAXSPEEDL):
                self.linear_drive("f", MAXSPEEDL, errorX, Kplf)
            else:
                self.linear_drive("f",int(math.floor(errorY*KplRide+BaseSpeedL)), errorX, Kplf)
       
        else:
            self.stop()
        



      #Example use##
# robot=Robot(21,20,16,26,19,13,24,18,23,17,22,27)
# time.sleep(5)
# robot.linear_drive("f",100,0,0)
# time.sleep(5)
# robot.linear_drive("b",100,0,0)
# time.sleep(5)
# robot.linear_drive("r",100,0,0)
# time.sleep(5)
# robot.linear_drive("l",100,0,0)
# time.sleep(5)
# robot.rotation_in_place("r",100)
# time.sleep(5)
# robot.rotation_in_place("l",100)
# time.sleep(5)
# robot.stop()