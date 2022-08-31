from operator import gt
import os
import time
import playsound
from gtts import gTTS
import pygame

tts = gTTS(text="Target found. Please show the correct gesture.",slow=False)
filename="Target found.mp3"
tts.save(filename)
pygame.mixer.init(28000)
pygame.mixer.music.load("/home/pi/Projekt/TrackingRobot/Target found.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True :
     continue

