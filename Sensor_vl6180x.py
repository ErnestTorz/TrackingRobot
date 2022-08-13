# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Demo of reading the range and lux from the VL6180x distance sensor and
# printing it every second.

import time

import board
import busio

import RPi.GPIO as GPIO


import adafruit_vl53l0x



#UP:   9 | 6
#     ------
#Down: 11| 5
class Range_Sensors:
    def __init__(self, Left_up, Right_up, Left_down, Right_down):
        self.Left_up    = Left_up 
        self.Right_up   = Right_up
        self.Left_down  = Left_down
        self.Right_down = Right_down
        
        GPIO.setup(Left_up,GPIO.OUT)
        GPIO.setup(Left_down,GPIO.OUT)
        GPIO.setup(Right_up,GPIO.OUT)
        GPIO.setup(Right_down,GPIO.OUT)

        GPIO.output(Left_up,GPIO.LOW)
        GPIO.output(Left_down,GPIO.LOW)
        GPIO.output(Right_up,GPIO.LOW)
        GPIO.output(Right_down,GPIO.LOW)

        self.i2c = busio.I2C(board.SCL, board.SDA)
        
        error=0
        try:
            error=1
            GPIO.output(Left_up,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor1 = adafruit_vl53l0x.VL53L0X(self.i2c)     
            self.sensor1.set_address(0x32)
            self.sensor1.start_continuous()

            error=2
            GPIO.output(Right_up,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor2 = adafruit_vl53l0x.VL53L0X(self.i2c)
            self.sensor2.set_address(0x34)
            self.sensor2.start_continuous()

            error=3
            GPIO.output(Left_down,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor3 = adafruit_vl53l0x.VL53L0X(self.i2c)
            self.sensor3.set_address(0x36)
            self.sensor3.start_continuous()

            error=4
            GPIO.output(Right_down,GPIO.HIGH)
            time.sleep(0.1)
            self.sensor4 = adafruit_vl53l0x.VL53L0X(self.i2c)
            self.sensor4.set_address(0x38)
            self.sensor4.start_continuous()
        except:
            print("Init sensor error: "+str(error))
            GPIO.output(Left_up,GPIO.LOW)
            GPIO.output(Left_down,GPIO.LOW)
            GPIO.output(Right_up,GPIO.LOW)
            GPIO.output(Right_down,GPIO.LOW)
        
    def reading (self):
        array=[]

        array.append(int(self.sensor1.range))
        time.sleep(0.01)
        array.append(int(self.sensor2.range))
        time.sleep(0.01)
        array.append(int(self.sensor3.range))
        time.sleep(0.01)
        array.append(int(self.sensor4.range))
       
        print(array)
        return array




# Sensors=Range_Sensors(1,6,5,12)
# while True:

#     readings=Sensors.reading()
#     print(str(readings[0])+"||"+str(readings[1]))
#     print("------------------------------------")
#     print(str(readings[2])+"||"+str(readings[3]))
#     print("\n \n")

#     # time.sleep(0.70)