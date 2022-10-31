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
    self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    self.cs = digitalio.DigitalInOut(board.D25)
    self.mcp = MCP.MCP3008(self.spi, self.cs)

    self.battery = AnalogIn(self.mcp, MCP.P2)
    self.sensor0 = AnalogIn(self.mcp, MCP.P4)
    self.sensor1 = AnalogIn(self.mcp, MCP.P5)
    self.sensor2 = AnalogIn(self.mcp, MCP.P6)
    self.sensor3 = AnalogIn(self.mcp, MCP.P7)

 def voltage(self):
    con=5.751 
    mesurements=[]
    for a in range(100):
        mesurements.append(copy.copy(round(self.battery.voltage,3)))
    #Odczyt napięcia na kanale oraz przeliczenie na napięcie na baterii
    #wykorzystując fakt wiedzy o urzytym dzielnku napięcia
    return round(con*median(mesurements),3)

 def reading (self):
    array=[]

    array.append(copy.copy(round(self.sensor0.voltage,3)))       
    array.append(copy.copy(round(self.sensor1.voltage,3)))    
    array.append(copy.copy(round(self.sensor2.voltage,3)))   
    array.append(copy.copy(round(self.sensor3.voltage,3)))
            
    return copy.copy(array)
