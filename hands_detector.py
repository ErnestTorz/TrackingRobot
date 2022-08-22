import cv2
import mediapipe
class Hand_detector:
  def __init__(self):

    self.handsModule = mediapipe.solutions.hands
    self.hand = self.handsModule.Hands(static_image_mode=False,min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=2) 
  
  def detect(self, frame_resized_colored):
    self.frame=frame_resized_colored
    results = self.hand.process(self.frame)
    if results.multi_hand_landmarks != None:
              for handLandmarks in results.multi_hand_landmarks:
                  
                  #Below is Added Code to find and print to the shell the Location X-Y coordinates of Index Finger, Uncomment if desired
                  count=0
                  for point in self.handsModule.HandLandmark:
                      # print(point)
                      normalizedLandmark = handLandmarks.landmark[point]
                      
                      
                    #   Using the Finger Joint Identification Image we know that point 8 represents the tip of the Index Finger
                      # if point == 8 :
                      #    #  print(point)
                      #    #  print(pixelCoordinatesLandmark[0])
                      #    print(normalizedLandmark.y)

                  if handLandmarks.landmark[4].y < handLandmarks.landmark[8].y:
                      print(handLandmarks.landmark[4].y)
                      print(handLandmarks.landmark[8].y)
                      print("YES") 


                          
                          
                      
                      