#Import the necessary Packages for this software to run

import mediapipe
import cv2
import hands_detector 
from threading import Thread
import copy

hander= hands_detector.Hand_detector()

#Use CV2 Functionality to create a Video stream and add some values
cap = cv2.VideoCapture(0)
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

pom_thread = 0
thread= None
#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
while True:
           ret, frame = cap.read()
           #Unedit the below line if your live feed is produced upsidedown
           #flipped = cv2.flip(frame, flipCode = -1)
           
           #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
           frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           frame1 = cv2.resize(frame_rgb, (640, 480))
           
        #    wynik=hander.detect(frame1)
           pom=-1
           pom=hander.run(frame1)

           if(pom==1):
                    print("tak")
           if(pom==-1):
                    print("-1")
         #   if(pom==0):
         #             print("nie")
        #    if (pom_thread == 0):   
        #     thread = Thread(target=hander.detect, args=(copy.copy(frame1))).start()
        #     pom_thread = 1

        #    if pom_thread==1:
        #     if ((Thread)(thread)).is_alive() == False:
        #          if(hander.ret_val()==1):
        #             print("tak")
        #          else:
        #              print("nie")
        #          thread = Thread(target=hander.detect, args=(copy.copy(frame1))).start()
           
           #Below shows the current frame to the desktop 
           cv2.imshow("Frame", frame);
           key = cv2.waitKey(1) & 0xFF
           
           #Below states that if the |q| is press on the keyboard it will stop the system
           if key == ord("q"):
              break