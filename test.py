#Import the necessary Packages for this software to run
import mediapipe
import cv2
import hands_detector 

hander= hands_detector.Hand_detector()

#Use CV2 Functionality to create a Video stream and add some values
cap = cv2.VideoCapture(0)
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')


#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
while True:
           ret, frame = cap.read()
           #Unedit the below line if your live feed is produced upsidedown
           #flipped = cv2.flip(frame, flipCode = -1)
           
           #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
           frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           frame1 = cv2.resize(frame_rgb, (640, 480))
           
           hander.detect(frame1)
           #Below shows the current frame to the desktop 
           cv2.imshow("Frame", frame);
           key = cv2.waitKey(1) & 0xFF
           
           #Below states that if the |q| is press on the keyboard it will stop the system
           if key == ord("q"):
              break