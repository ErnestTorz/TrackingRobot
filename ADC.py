# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from xml.etree.ElementInclude import include
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import copy
import time
from statistics import median

class ADC:

 def __init__(self):
# create the spi bus
    self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
    self.cs = digitalio.DigitalInOut(board.D25)

# create the mcp object
    self.mcp = MCP.MCP3008(self.spi, self.cs)

# create an analog input channel on pin 0
    self.battery = AnalogIn(self.mcp, MCP.P2)
    self.sensor0 = AnalogIn(self.mcp, MCP.P4)
    self.sensor1 = AnalogIn(self.mcp, MCP.P5)
    self.sensor2 = AnalogIn(self.mcp, MCP.P6)
    self.sensor3 = AnalogIn(self.mcp, MCP.P7)


 def voltage(self):
    # R2=950
    # R1=4500
    # con=1/0.17215556
    mesurements=[]
    for a in range(100):
        mesurements.append(copy.copy(round(self.battery.voltage,3)))
    # mesurements.sort()   
    con=5.751 
    # print("Raw ADC Value: ", chan.value)
    # print("ADC Voltage: " + str(chan.voltage) + "V")
    # print(chan.voltage*(R1+R2)/R2)
    # print(con*chan.voltage)

    
    return round(con*median(mesurements),3)

 def reading (self):
        array=[]

        array.append(copy.copy(round(self.sensor0.voltage,3)))
        
        array.append(copy.copy(round(self.sensor1.voltage,3)))
     
        array.append(copy.copy(round(self.sensor2.voltage,3)))
    
        array.append(copy.copy(round(self.sensor3.voltage,3)))
            
        return copy.copy(array)

# ports = ADC()
# border=1.4
# while True:
    # print(ports.reading())
    #  print(ports.voltage())
    # time.sleep(0.2)
    # for a in (ports.reading()):
    #     if a >= 1.5 :
    #         print ("tak")
    
    # print()