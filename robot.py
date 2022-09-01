
from threading import Thread
import RPi.GPIO as GPIO
import math
# import Sensor_VL53L0X
from ADC import ADC
import time
import copy


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


        # self.flaga_detect_1=0
        # self.flaga_detect_2=0
        # self.flaga_detect_3=0
        # self.flaga_detect_4=0

        self.counter_1=0
        self.counter_2=0
        self.counter_3=0
        self.counter_4=0
        self.counter_5=0
  

        # while(True):
        #  self.Sensors=Sensor_VL53L0X.Range_Sensors(1,6,5,12)
        #  if self.Sensors.Error == False :
        #     break
        
        # self.readings= self.Sensors.reading()
        self.ADC=ADC()
        self.readings=self.ADC.reading()

        time.sleep(1)
        # self.ADC=ADC()
        print("Battery voltage:"+str(self.ADC.voltage()))


    
    def __del__(self):
        GPIO.cleanup()
    
    def run(self, frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax):
        if (self.pom_thread == 0):
            # if self.Sensors.lock==False:
                # if(self.Sensors.sensor1.data_ready and self.Sensors.sensor2.data_ready and self.Sensors.sensor3.data_ready and self.Sensors.sensor4.data_ready ):
                #  self.readings= self.Sensors.reading()
            self.readings=self.ADC.reading()
            self.thread = Thread(target=self.robot_controler, args=(frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax)).start()
            self.pom_thread = 1

        if self.pom_thread==1:
            if ((Thread)(self.thread)).is_alive() == False:
                # if self.Sensors.lock==False:
                    # if(self.Sensors.sensor1.data_ready and self.Sensors.sensor2.data_ready and self.Sensors.sensor3.data_ready and self.Sensors.sensor4.data_ready ):
                    # self.readings= self.Sensors.reading()
                self.readings=self.ADC.reading()
                    # print(self.readings)
                
                self.thread = Thread(target=self.robot_controler, args=(frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax)).start()
    
    def  obstacle_detection(self):
        self.obstacle_flaga=False
        # detection_distance=160
        # min_distance=15
        detection_distance=3.3
        min_distance=0.7
        counter_boundary=4
    
    
        # if(self.Sensors.Error==False):   
        if(self.direction==FORWARD and self.readings[0]>min_distance and self.readings[0]<= detection_distance and (self.readings[1]<min_distance or self.readings[1]> detection_distance)):
                # if self.counter_1 ==0:
                #  self.counter_1+=1
                # #  self.sensor_save_1=copy.copy(self.readings)

                # # if (self.readings[0]<=self.sensor_save_1[0]+5 and self.readings[0]>=self.sensor_save_1[0]-5):
                # else:
                self.counter_1+=1
                # else:
                #   self.counter_1=0

                if(self.counter_1>counter_boundary):
                    self.obstacle_flaga=True
                    # if(self.flaga_detect_1==0):
                        # self.start1=time.time()
                        # self.stop_without_record()
                    self.flaga_detect_1=1
                    # if(time.time()-self.start1<1.5  and self.readings[0]>min_distance and self.readings[0]< detection_distance):
                        # print("1: "+str(time.time()-self.start1))
                    # if (time.time()-self.start1>=1   and self.readings[0]>min_distance and self.readings[0]< detection_distance  and (self.readings[1]<min_distance or self.readings[1]> detection_distance )):
                    self.linear_drive("r",90,0,0)
                    print("F_R")
        else:
                if(self.counter_1>counter_boundary):
                    self.stop_without_record()
                    # time.sleep(0.5)
                # self.flaga_detect_1=0
                # self.start1=0
                self.counter_1=0


       
           
        if(self.direction==FORWARD and self.readings[1]>min_distance and self.readings[1]<= detection_distance and (self.readings[0]<min_distance or self.readings[0]> detection_distance)):
                # if self.counter_2 ==0:
                #  self.counter_2+=1
                # #  self.sensor_save_2=copy.copy(self.readings)

                # # if (self.readings[1]<=self.sensor_save_2[1]+5 and self.readings[1]>=self.sensor_save_2[1]-5):
                # else:
                self.counter_2+=1
                # else:
                #   self.counter_2=0
                if(self.counter_2>counter_boundary):
                    self.obstacle_flaga=True
                    # if(self.flaga_detect_2==0):
                        # self.start2=time.time()
                        # self.stop_without_record()
                        # self.flaga_detect_2=1
                    # if(time.time()-self.start2<0.75    and self.readings[1]>min_distance and self.readings[1]< detection_distance):
                        # print("2: "+str(time.time()-self.start2))
                    # if (time.time()-self.start2>=1   and self.readings[1]>min_distance and self.readings[1]< detection_distance  and (self.readings[0]<min_distance or self.readings[0]> detection_distance )):
                    self.linear_drive("l",90,0,0)
                    print("F_L")
        else:
                if(self.counter_2>counter_boundary):
                    self.stop_without_record()
                    # time.sleep(0.5)
                # self.flaga_detect_2=0
                # self.start2=0
                self.counter_2=0


         
        if(self.direction==BACKWARD and self.readings[2]>min_distance and self.readings[2]<= detection_distance and (self.readings[3]<min_distance or self.readings[3]> detection_distance)):
                self.counter_3+=1
                if(self.counter_3>counter_boundary):
                    self.obstacle_flaga=True
                    # if(self.flaga_detect_3==0):
                        #  self.start3=time.time()
                        #  self.stop_without_record()
                        #  self.flaga_detect_3=1
                    # if(time.time()<0.75 -self.start3 and self.readings[2]>min_distance and self.readings[2]< detection_distance  ):
                        #    print("3: "+str(time.time()-self.start3))
                    # if (time.time()-self.start3>=1   and self.readings[2]>min_distance and self.readings[2]< detection_distance  and (self.readings[3]<min_distance or self.readings[3]> detection_distance )):
                    self.linear_drive("r",90,0,0)
                    print("B_R")
        else:
                if(self.counter_3>counter_boundary):
                    self.stop_without_record()
                    # time.sleep(0.5)
                # self.flaga_detect_3=0
                # self.start3=0
                self.counter_3=0
        

        
        if(self.direction==BACKWARD and self.readings[3]>min_distance and self.readings[3]<= detection_distance and (self.readings[2]<min_distance or self.readings[2]> detection_distance)):
                self.counter_4+=1
                if(self.counter_4>counter_boundary):
                    self.obstacle_flaga=True
                    # if(self.flaga_detect_4==0): 
                        # self.start4=time.time()
                        # self.stop_without_record()
                        # self.flaga_detect_4=1
                    # if(time.time()-self.start4<0.75  and self.readings[3]>min_distance and self.readings[3]< detection_distance  ):
                        # print("4: "+str(time.time()-self.start4))
                        # print(self.readings)
                   
                    self.linear_drive("l",90,0,0)
                    print("B_L")
        else:
                if(self.counter_4>counter_boundary):
                    self.stop_without_record()
                    # time.sleep(0.5)
                # self.flaga_detect_4=0
                # self.start4=0
                self.counter_4=0
        
         
        if(self.direction==BACKWARD and self.readings[2]>min_distance and self.readings[2]<= detection_distance and self.readings[3]>min_distance and self.readings[3]<= detection_distance):
            self.counter_5+=1
            if(self.counter_5>counter_boundary):
                self.stop_without_record()
                self.obstacle_flaga=True
                print("B_S")
        else:
            self.counter_5=0

        # else:
        #     self.obstacle_flaga=True
        #     self.stop_without_record()
            

                
            
        
    def stop_without_record (self):
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
                
    def stop (self):
        self.direction=STOP
        self.obstacle_detection()
        if(self.obstacle_flaga==False):
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
                    self.obstacle_detection()
                   
                    if(self.obstacle_flaga==False):
                        
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
                    self.direction=BACKWARD
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
                #self.direction=RIGHT
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
                self.obstacle_detection()
                if(self.obstacle_flaga==False):
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
                self.obstacle_detection()
                if(self.obstacle_flaga==False):
                   
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

                # if(self.flaga_detect_4==0 and self.flaga_detect_3 ==0):
                #     time.sleep(0.5)
    
    def robot_controler(self, frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax):
        ####LINIOWA JAZDA#####
        Kplf = 50   #Wzmocnienie jazdy do [przodu], szybkosc korekcji ruchu lewo/prawo
        Kplb = Kplf #Wzmocnienie jazdy do  [tylu] , szybkosc korekcji ruchu lewo/prawo
       
        KplRide=35    #Wzmocnienie do regulowania predkosci im obiekt jest bardziej w skrajnej pozycji tym predkosc bedzie wieksza
        BaseSpeedL=65 #Bazowa startowa, a zarazem minimalna predkosc
        MAXSPEEDL=95  #Predkosc maksymalna

        #####ROTACJA######
        Kpr= 40       #Wzmocnienie do regulowania predkosci im obiekt jest bardziej w skrajnej pozycji tym predkosc bedzie wieksza
        BaseSpeedR=65 #Bazowa startowa, a zarazem minimalna predkosc
        MAXSPEEDR=90  #Predkosc maksymalna
        
        #Sprawdzenie czy obiekt znajduje sie znacząco na prawo
        if object_x_center >= (frame_x_size / 5) * 3: 
            errorX=(object_x_center-((frame_x_size / 5) * 3))/(frame_x_size-((frame_x_size / 5) * 3))
            if(errorX*Kpr+BaseSpeedR>MAXSPEEDR):
                self.rotation_in_place('r',MAXSPEEDR)
            else:
                self.rotation_in_place('r',int(math.floor(errorX*Kpr+BaseSpeedR)))
        
        #Sprawdzenie czy obiekt znajduje sie znacząco na lewo
        elif object_x_center <= (frame_x_size / 5) * 2:
            errorX=(((frame_x_size / 5) * 2)-object_x_center)/((frame_x_size / 5) * 2)
            if(errorX*Kpr+BaseSpeedR>MAXSPEEDR):
                self.rotation_in_place('l',MAXSPEEDR)
            else:
                self.rotation_in_place('l',int(math.floor(errorX*Kpr+BaseSpeedR)))

        #Sprawdzenie czy obiekt znajduje sie znacząco za blisko
        elif ((float)(ymax - ymin)) / frame_y_size > 0.95:
            errorX = ((frame_x_size / 2) - object_x_center) / (frame_x_size / 2)
            errorY=((((float)(ymax - ymin)) / frame_y_size)-0.95)/(1-0.95)
            if(errorY*KplRide+BaseSpeedL>MAXSPEEDL):
                self.linear_drive("b", MAXSPEEDL, errorX, Kplb)
            else:
                self.linear_drive("b",int(math.floor(errorY*KplRide+BaseSpeedL)), errorX, Kplb)

        #Sprawdzenie czy obiekt znajduje sie znacząco za dalaeko
        elif ((float)(ymax - ymin)) / frame_y_size < 0.85:
            errorX = ((frame_x_size / 2) - object_x_center) / (frame_x_size / 2)
            errorY=(85-(((float)(ymax - ymin)) / frame_y_size))/(85)
            if(errorY*KplRide+BaseSpeedL>MAXSPEEDL):
                self.linear_drive("f", MAXSPEEDL, errorX, Kplf)
            else:
                self.linear_drive("f",int(math.floor(errorY*KplRide+BaseSpeedL)), errorX, Kplf)
       
       #Robot nie ma potrzeby korekcji pozycji wiec czeka
        else:
            self.stop()
    
    def test(self):
        GPIO.output(self.A_in1, GPIO.LOW)
        GPIO.output(self.A_in4, GPIO.LOW)
        GPIO.output(self.A_in2, GPIO.HIGH)
        GPIO.output(self.A_in3, GPIO.HIGH)

        GPIO.output(self.B_in2, GPIO.LOW)
        GPIO.output(self.B_in3, GPIO.LOW)
        GPIO.output(self.B_in1, GPIO.HIGH)
        GPIO.output(self.B_in4, GPIO.HIGH)
        # GPIO.output(self.B_in1, GPIO.LOW)
        # GPIO.output(self.B_in4, GPIO.LOW)
        # GPIO.output(self.B_in2, GPIO.HIGH)
        # GPIO.output(self.B_in3, GPIO.HIGH)
        self.B_pwmB.ChangeDutyCycle(100)
        self.B_pwmA.ChangeDutyCycle(100)
        self.A_pwmB.ChangeDutyCycle(100)
        self.A_pwmA.ChangeDutyCycle(100)



     # #Example use
# robot=Robot(21,20,16,26,19,13,24,18,23,17,22,27)
# time.sleep(5)
# robot.linear_drive("f",100,0,0)
# time.sleep(5)
# time.sleep(5)
# robot.linear_drive("b",100,0,0)
# # robot.test()
# time.sleep(10)
# robot.linear_drive("r",100,0,0)
# time.sleep(5)
# robot.linear_drive("l",100,0,0)
# time.sleep(5)
# robot.rotation_in_place("r",100)
# time.sleep(5)
# robot.rotation_in_place("l",100)
# time.sleep(5)
# robot.stop()