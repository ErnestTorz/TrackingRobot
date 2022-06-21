from threading import Thread
import RPi.GPIO as GPIO
import math


class Robot:
    def __init__(self, ena, in1, in2, in3, in4, enb):
        self.ena = ena
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        self.enb = enb
        self.frequency = 500
        self.pom_thread = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(ena, GPIO.OUT)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        self.pwmA = GPIO.PWM(ena, self.frequency)
        self.pwmA.start(0)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)
        GPIO.setup(enb, GPIO.OUT)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
        self.pwmB = GPIO.PWM(enb, self.frequency)
        self.pwmB.start(0)
    
    def __del__(self):
        GPIO.cleanup()
    
    def run(self, frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax):
        if self.pom_thread == 0:
            self.thread = Thread(target=self.robot_controler, args=(frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax)).start()
            self.pom_thread = 1
        if ((Thread)(self.thread)).is_alive() == False:
             self.thread = Thread(target=self.robot_controler, args=(frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax)).start()

    def stop (self):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def linear_drive(self, direction, speed, error, Kp):
        minspeed = 70.00
        maxspeed = 100.00
        if isinstance(speed, int) and (100 >= speed >= 0):
            if direction == "forward" or direction == "Forward" or direction == "f" or direction == "F":
                GPIO.output(self.in2, GPIO.LOW)
                GPIO.output(self.in3, GPIO.LOW)
                GPIO.output(self.in1, GPIO.HIGH)
                GPIO.output(self.in4, GPIO.HIGH)
                if (speed + (error * Kp)) >= maxspeed:
                    self.pwmA.ChangeDutyCycle(maxspeed)
                elif(speed + (error * Kp)) <= minspeed:
                    self.pwmA.ChangeDutyCycle(minspeed)
                else:
                    print(speed + (error * Kp))
                    self.pwmA.ChangeDutyCycle(speed + (error * Kp))

                if(speed - (error * Kp)) > maxspeed:
                    self.pwmB.ChangeDutyCycle(maxspeed)
                elif(speed - (error * Kp)) < minspeed:
                    self.pwmB.ChangeDutyCycle(minspeed)
                else:
                    self.pwmB.ChangeDutyCycle(speed - (error * Kp))
            elif direction == "backward" or direction == "Backward" or direction == "b" or direction == "B":
                GPIO.output(self.in1, GPIO.LOW)
                GPIO.output(self.in4, GPIO.LOW)
                GPIO.output(self.in2, GPIO.HIGH)
                GPIO.output(self.in3, GPIO.HIGH)
                if(speed - (error * Kp)) > maxspeed:
                    self.pwmA.ChangeDutyCycle(maxspeed)
                elif(speed - (error * Kp)) < minspeed:
                    self.pwmA.ChangeDutyCycle(minspeed)
                else:
                    self.pwmA.ChangeDutyCycle(speed - (error * Kp))

                if(speed + (error * Kp)) > maxspeed:
                    self.pwmB.ChangeDutyCycle(maxspeed)
                elif(speed + (error * Kp)) < minspeed:
                    self.pwmB.ChangeDutyCycle(minspeed)
                else:
                    self.pwmB.ChangeDutyCycle(speed + (error * Kp))

    def rotation_in_place(self, direction, speed):
        if isinstance(speed, int) and (100 >= speed >= 0):
            if direction == "left" or direction == "Left" or direction == "l" or direction == "L":
                GPIO.output(self.in2, GPIO.LOW)
                GPIO.output(self.in4, GPIO.LOW)
                GPIO.output(self.in1, GPIO.HIGH)
                GPIO.output(self.in3, GPIO.HIGH)
                self.pwmA.ChangeDutyCycle(speed)
                self.pwmB.ChangeDutyCycle(speed)
            elif direction == "right" or direction == "Right" or direction == "r" or direction == "R":
                GPIO.output(self.in1, GPIO.LOW)
                GPIO.output(self.in3, GPIO.LOW)
                GPIO.output(self.in2, GPIO.HIGH)
                GPIO.output(self.in4, GPIO.HIGH)
                self.pwmA.ChangeDutyCycle(speed)
                self.pwmB.ChangeDutyCycle(speed)
    
    def robot_controler(self, frame_x_size, frame_y_size, object_x_center, object_y_center, xmin, xmax, ymin, ymax):
        Kplf = 50
        Kplb = 50
        if object_x_center >= (frame_x_size / 5) * 3:
            self.rotation_in_place('r', 100)

        elif object_x_center <= (frame_x_size / 5) * 2:
            self.rotation_in_place('l', 100)

        elif ((float)(ymax - ymin)) / frame_y_size > 0.75:
            errorX = ((frame_x_size / 2) - object_x_center) / (frame_x_size / 2)
            self.linear_drive("b", 100, errorX, Kplb)

        elif ((float)(ymax - ymin)) / frame_y_size < 0.65:
            errorX = ((frame_x_size / 2) - object_x_center) / (frame_x_size / 2)
            self.linear_drive("f", 100, errorX, Kplf)
        else:
            self.stop()
