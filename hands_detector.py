import cv2
import mediapipe
from operator import length_hint
import math
from threading import Thread
import copy
thread=None
class Hand_detector:
  
  def __init__(self):
    self.handsModule= mediapipe.solutions.hands 
    self.hand =self.handsModule.Hands(static_image_mode=False,min_detection_confidence=0.53, min_tracking_confidence=0.53, max_num_hands=2) 

  def detect(self,img):
    
    results = self.hand.process(img)
    
    if results.multi_hand_landmarks != None:
        if(length_hint(results.multi_hand_landmarks)==2):
                MHL04x= results.multi_hand_landmarks[0].landmark[4].x
                MHL02x= results.multi_hand_landmarks[0].landmark[2].x
                MHL04y= results.multi_hand_landmarks[0].landmark[4].y
                MHL02y= results.multi_hand_landmarks[0].landmark[2].y
                reference_distance_thumb = (((MHL04x - MHL02x)**2 + (MHL04y - MHL02y)**2)**0.5)
                
                MHL08x= results.multi_hand_landmarks[0].landmark[8].x
                MHL18x= results.multi_hand_landmarks[1].landmark[8].x
                MHL08y= results.multi_hand_landmarks[0].landmark[8].y
                MHL18y= results.multi_hand_landmarks[1].landmark[8].y
                #Sprawdenie czy czubki kciukw sa przy sobie
                if((((MHL08x - MHL18x)**2 + (MHL08y - MHL18y)**2)**0.5)<=reference_distance_thumb):
                      MHL016y= results.multi_hand_landmarks[0].landmark[16].y
                      MHL015y= results.multi_hand_landmarks[0].landmark[15].y
                      #Sprawdenie czy palce ręki nr.0 skierowane są w góre
                      if(MHL016y<MHL015y):
                        MHL116y= results.multi_hand_landmarks[1].landmark[16].y
                        MHL115y= results.multi_hand_landmarks[1].landmark[15].y
                        #Sprawdenie czy palce ręki nr.1 skierowane są w góre
                        if(MHL116y<MHL115y):
                          return [1,results.multi_hand_landmarks] 
        return [2, results.multi_hand_landmarks]  
    return [0,None]  
                   