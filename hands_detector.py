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
    self.hand =self.handsModule.Hands(static_image_mode=True,min_detection_confidence=0.65, min_tracking_confidence=0.65, max_num_hands=2) 
    # self.ret=-1
    # self.pom_thread=0
    # self.memory=0
    # self.thread =None
  

  # def run(self,frame_resized_colored):
  #   global thread
  #   if (self.pom_thread == 0): 
  #           self.img=frame_resized_colored 
  #           thread = Thread(target=self.detect).start()
  #           self.pom_thread = 1
  #           return -1
            

  #   if self.pom_thread==1:
  #     # Thread(self.thread).join()
  #     if  (Thread(thread).is_alive())== False:
         
  #        self.memory=copy.copy(self.ret)
  #        self.img=frame_resized_colored
  #        thread = Thread(target=self.detect).start()
  #        return self.memory
  #     else:
  #      return -1
         
      

  def detect(self,img):
    # self.ret=0
    
    results = self.hand.process(img)
    
    if results.multi_hand_landmarks != None:
        if(length_hint(results.multi_hand_landmarks)==2):
                # self.ret=1  
                reference_distance_thumb = (((results.multi_hand_landmarks[0].landmark[4].x - results.multi_hand_landmarks[0].landmark[2].x)**2 + (results.multi_hand_landmarks[0].landmark[4].y - results.multi_hand_landmarks[0].landmark[2].y)**2)**0.5)
                #Sprawdenie czy czubki kciukw sa przy sobie
                if((((results.multi_hand_landmarks[0].landmark[8].x - results.multi_hand_landmarks[1].landmark[8].x)**2 + (results.multi_hand_landmarks[0].landmark[8].y - results.multi_hand_landmarks[1].landmark[8].y)**2)**0.5)<=reference_distance_thumb):
                      print("1")
                  
                  # reference_distance_wide=(((results.multi_hand_landmarks[0].landmark[0].x - results.multi_hand_landmarks[0].landmark[9].x)**2 + (results.multi_hand_landmarks[0].landmark[0].y - results.multi_hand_landmarks[0].landmark[9].y)**2)**0.5)
                  #sprawdzenie czy rence sa frontem do kamery
                  # if((math.fabs(results.multi_hand_landmarks[0].landmark[5].x-results.multi_hand_landmarks[0].landmark[17].x))/3)<=reference_distance_wide:                  
                    # if((math.fabs(results.multi_hand_landmarks[1].landmark[5].x-results.multi_hand_landmarks[1].landmark[17].x))/3)<=reference_distance_wide:
                      #sprawdzenie czy czubki palcow skierowane sa do gory
                      # print("2")
                      if(results.multi_hand_landmarks[0].landmark[16].y<results.multi_hand_landmarks[0].landmark[15].y):
                        if(results.multi_hand_landmarks[1].landmark[16].y<results.multi_hand_landmarks[1].landmark[15].y):
                          print("3")
                          #sprawdzenie czy palce kciukow sa w miate poziome
                          # horizontaly_distance=(((results.multi_hand_landmarks[0].landmark[5].x - results.multi_hand_landmarks[0].landmark[17].x)**2 + (results.multi_hand_landmarks[0].landmark[5].y - results.multi_hand_landmarks[0].landmark[17].y)**2)**0.5)
                          # horizontaly_distance=horizontaly_distance*(2/3)
                          # if(((results.multi_hand_landmarks[0].landmark[5].x - results.multi_hand_landmarks[0].landmark[4].x)**2 + (results.multi_hand_landmarks[0].landmark[5].y - results.multi_hand_landmarks[0].landmark[4].y)**2)**0.5)>horizontaly_distance:
                            # if(((results.multi_hand_landmarks[1].landmark[5].x - results.multi_hand_landmarks[1].landmark[4].x)**2 + (results.multi_hand_landmarks[1].landmark[5].y - results.multi_hand_landmarks[1].landmark[4].y)**2)**0.5)>horizontaly_distance:
                          return [1,results.multi_hand_landmarks]
                              # self.ret=1  
        return [2, results.multi_hand_landmarks]  
    return [0,None]  
     
  
        



                          
                          
                      
                      