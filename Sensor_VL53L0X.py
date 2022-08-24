# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# #Demo of reading the range and lux from the VL6180x distance sensor and
# printing it every second.

from itertools import count
from pickle import TRUE
import time

import board
import busio
import copy
import RPi.GPIO as GPIO
import math


import adafruit_vl53l0x



#UP:   9 | 6
#     ------
#Down: 11| 5
class Range_Sensors:
    def Error_handler(self):
        print("Attempting to reconnect I2C sensors")

        GPIO.output(self.Left_up,GPIO.LOW)
        GPIO.output(self.Left_down,GPIO.LOW)
        GPIO.output(self.Right_up,GPIO.LOW)
        GPIO.output(self.Right_down,GPIO.LOW)

        time.sleep(0.2)

        self.i2c = busio.I2C(board.SCL, board.SDA)
        
        error=0
        
        try:
            error=1
            GPIO.output(self.Left_up,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor1 = adafruit_vl53l0x.VL53L0X(self.i2c)     
            self.sensor1.set_address(0x32)
            self.sensor1.measurement_timing_budget=50000
            self.sensor1.start_continuous()

            error=2
            GPIO.output(self.Right_up,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor2 = adafruit_vl53l0x.VL53L0X(self.i2c)
            self.sensor2.set_address(0x34)
            self.sensor2.measurement_timing_budget=50000
            self.sensor2.start_continuous()

            error=3
            GPIO.output(self.Left_down,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor3 = adafruit_vl53l0x.VL53L0X(self.i2c)
            self.sensor3.set_address(0x36)
            self.sensor3.measurement_timing_budget=50000
            self.sensor3.start_continuous()

            error=4
            GPIO.output(self.Right_down,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor4 = adafruit_vl53l0x.VL53L0X(self.i2c)
            self.sensor4.set_address(0x38)
            self.sensor4.measurement_timing_budget=50000
            self.sensor4.start_continuous()
            
        except:
            print("Reconection failed. Sensor error: "+str(error))
            GPIO.output(self.Left_up,GPIO.LOW)
            GPIO.output(self.Left_down,GPIO.LOW)
            GPIO.output(self.Right_up,GPIO.LOW)
            GPIO.output(self.Right_down,GPIO.LOW)
            self.Error=True

    def __init__(self, Left_up, Right_up, Left_down, Right_down):
        self.Error=True
        
        self.lock=False

        self.Left_up    = Left_up 
        self.Right_up   = Right_up
        self.Left_down  = Left_down
        self.Right_down = Right_down
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(Left_up,GPIO.OUT)
        GPIO.setup(Left_down,GPIO.OUT)
        GPIO.setup(Right_up,GPIO.OUT)
        GPIO.setup(Right_down,GPIO.OUT)

        GPIO.output(Left_up,GPIO.LOW)
        GPIO.output(Left_down,GPIO.LOW)
        GPIO.output(Right_up,GPIO.LOW)
        GPIO.output(Right_down,GPIO.LOW)

        time.sleep(0.5)

        self.i2c = busio.I2C(board.SCL, board.SDA)
        
        error=0
        
        try:
            error=1
            GPIO.output(Left_up,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor1 = adafruit_vl53l0x.VL53L0X(self.i2c)     
            self.sensor1.set_address(0x32)
            self.sensor1.measurement_timing_budget=50000
            self.sensor1.start_continuous()

            error=2
            GPIO.output(Right_up,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor2 = adafruit_vl53l0x.VL53L0X(self.i2c)
            self.sensor2.set_address(0x34)
            self.sensor2.measurement_timing_budget=50000
            self.sensor2.start_continuous()

            error=3
            GPIO.output(Left_down,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor3 = adafruit_vl53l0x.VL53L0X(self.i2c)
            self.sensor3.set_address(0x36)
            self.sensor3.measurement_timing_budget=50000
            self.sensor3.start_continuous()

            error=4
            GPIO.output(Right_down,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor4 = adafruit_vl53l0x.VL53L0X(self.i2c)
            self.sensor4.set_address(0x38)
            self.sensor4.measurement_timing_budget=50000
            self.sensor4.start_continuous()
            self.Error=False
        except:
            print("Init sensor error: "+str(error))
            GPIO.output(Left_up,GPIO.LOW)
            GPIO.output(Left_down,GPIO.LOW)
            GPIO.output(Right_up,GPIO.LOW)
            GPIO.output(Right_down,GPIO.LOW)
            self.Error=True
        
    def reading (self):
        array=[]
        self.lock=True
        try:
            array.append(int(copy.copy(self.sensor1.range)))
       
            array.append(int(copy.copy(self.sensor2.range)))
     
            array.append(int(copy.copy(self.sensor3.range)))
    
            array.append(int(copy.copy(self.sensor4.range)))
            
            self.Error=False
        except:
            self.Error=True
            
            print("Reading data from sensor error !")
            array=[]
            array.append(0)
            array.append(0)
            array.append(0)
            array.append(0)
            self.Error_handler()

        self.lock=False
        return copy.copy(array)




# Sensors=Range_Sensors(1,6,5,12)
# detection_distance=140
# count_1=0
# count_2=0
# count_3=0
# count_4=0
# while True:

#     readings=Sensors.reading()
#     print(str(readings[0])+"||"+str(readings[1]))
#     print("------------------------------------")
#     print(str(readings[2])+"||"+str(readings[3]))
#     print("\n \n")
    # if(readings[3]>70 and readings[3]<= detection_distance and (readings[2]<70 or readings[2]> detection_distance)):
    #     count_1+=1
    #     if(count_1>4):
    #         print("3\n")
    #         print(readings)
    # else:
    #     count_1=0
    # if(readings[2]>70 and readings[2]<= detection_distance and (readings[3]<70 or readings[3]> detection_distance)):
    #     count_2+=1
        
    #     if(count_2>4):
    #         print("2\n")
    #         print(readings)
    # else:
    #         count_2=0
    # if(readings[0]>70 and readings[0]<= detection_distance and (readings[1]<70 or readings[1]> detection_distance)):
    #     count_3=count_3+1
    #     print (count_3)
    #     if(count_3>4):
    #          print("0\n")
    #          print(readings)
    # else:
    #          count_3=0
    # if(readings[1]>70 and readings[1]<= detection_distance and (readings[0]<70 or readings[0]> detection_distance)):
    #     count_4+=1
    #     if(count_4>4):
    #         print("1\n")
    #         print(readings)
    # else:
    #          count_4=0

    # print("---")