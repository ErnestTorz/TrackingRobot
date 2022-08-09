# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Demo of reading the range and lux from the VL6180x distance sensor and
# printing it every second.

import time

import board
import busio

import RPi.GPIO as GPIO


import adafruit_vl53l0x

GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)

GPIO.output(5,GPIO.LOW)
GPIO.output(6,GPIO.LOW)
GPIO.output(9,GPIO.LOW)
GPIO.output(11,GPIO.LOW)

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor instance.
GPIO.output(6,GPIO.HIGH)
time.sleep(0.1)
sensor1 = adafruit_vl53l0x.VL53L0X(i2c)
sensor1.set_address(0x32)

GPIO.output(5,GPIO.HIGH)
time.sleep(0.1)
sensor2 = adafruit_vl53l0x.VL53L0X(i2c)
sensor2.set_address(0x34)

GPIO.output(11,GPIO.HIGH)
time.sleep(0.1)
sensor3 = adafruit_vl53l0x.VL53L0X(i2c)
sensor3.set_address(0x36)

GPIO.output(9,GPIO.HIGH)
time.sleep(0.1)
sensor4 = adafruit_vl53l0x.VL53L0X(i2c)
sensor4.set_address(0x38)
# You can add an offset to distance measurements here (e.g. calibration)
# Swapping for the following would add a +10 millimeter offset to measurements:
# sensor = adafruit_vl6180x.VL6180X(i2c, offset=10)

# Main loop prints the range and lux every second:
while True:
    # Read the range in millimeters and print it.
    # range_mm = sensor.range
    # print("Range: {0}mm".format(range_mm))
    # Read the light, note this requires specifying a gain value:
    # - adafruit_vl6180x.ALS_GAIN_1 = 1x
    # - adafruit_vl6180x.ALS_GAIN_1_25 = 1.25x
    # - adafruit_vl6180x.ALS_GAIN_1_67 = 1.67x
    # - adafruit_vl6180x.ALS_GAIN_2_5 = 2.5x
    # - adafruit_vl6180x.ALS_GAIN_5 = 5x
    # - adafruit_vl6180x.ALS_GAIN_10 = 10x
    # - adafruit_vl6180x.ALS_GAIN_20 = 20x
    # - adafruit_vl6180x.ALS_GAIN_40 = 40x
    # light_lux = sensor.read_lux(adafruit_vl6180x.ALS_GAIN_1)
    # print("Light (1x gain): {0}lux".format(light_lux))
    # Delay for a second.
    print(str(sensor4.range)+"||"+str(sensor1.range))
    print("------------------------------------")
    print(str(sensor3.range)+"||"+str(sensor2.range))
    print("\n \n")

    time.sleep(0.70)