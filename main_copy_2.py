from threading import Thread
from turtle import delay
from Object import object
from robot import Robot
import importlib.util
import numpy as np
import argparse
import time
import cv2
import os
import math
from hands_detector import Hand_detector
import pygame as audio
import mediapipe
drawingModule = mediapipe.solutions.drawing_utils

robot = Robot(21,20,16,26,19,13,24,18,23,17,22,27)
Gesture= Hand_detector()
audio.mixer.init(26500)

class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self, resolution=(640, 480), framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])
            
        ## Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

        # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
        # Start the thread that reads frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # Return the most recent frame
        return self.frame

    def stop(self):
        # Indicate that the camera and thread should be stopped
        self.stopped = True


# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    required=True)
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.6)
parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                    default='360x300')  # 1280x720 tez dobra, 400x300
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()

MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
min_conf_threshold = float(args.threshold)
resW, resH = args.resolution.split('x')
imW, imH = int(resW), int(resH)
use_TPU = args.edgetpu

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
    if GRAPH_NAME == 'detect.tflite':
        GRAPH_NAME = 'edgetpu.tflite'       

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" 
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
# If using Edge TPU, use special load_delegate argument
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print("Path to interpreter: " + PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

# Check output layer name to determine if this model was created with TF2 or TF1,
# because outputs are ordered differently for TF2 and TF1 models
outname = output_details[0]['name']

if 'StatefulPartitionedCall' in outname:  # This is a TF2 model
    boxes_idx, classes_idx, scores_idx = 1, 3, 0
else:  # This is a TF1 model
    boxes_idx, classes_idx, scores_idx = 0, 1, 2

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# Initialize video stream
videostream = VideoStream(resolution=(imW, imH), framerate=30).start()
time.sleep(1)

cv2.namedWindow("Robot",cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("Robot",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

# For frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
detection_list = []
object_to_follow = object(imW / 2,imH / 2,  0, imW, 0, imH)
next_object = object(0, 0, 0, 0, 0, 0)
min_distance = math.inf
find_flag=False
timer=-math.inf
timer_zero=math.inf
delay_timer=-math.inf
gesture_flag=False

Flaga_posrednia=False
Main_flaga=False
Colision_person=None

Obszar_xmin=None
Obszar_xmax=None
Obszar_ymin=None
Obszar_ymax=None
Flaga_lewo=False
Flaga_prawo=False

delay_waiter=0

posredni_timer=None
Kp = 0.5

while True:
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()
   
    # Grab frame from video stream
    frame1 = videostream.read()

    # Acquire frame and resize to expected shape [1xHxWx3]
    frame = frame1.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)
    
    # Jesli miedzy wykrywaniem celu nie bylo przestoju wiekszego niz 5 sek (jesli prawda nie mozna uznac ze zgubiono cel) lub sledzona osoba wykonala gest w celu 
    # przestania sledzenia
    
    if(Flaga_posrednia==False):
        if((time.time()-timer) < 5):
            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()

            # Retrieve detection results
            boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0]  # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]  # Class index of detected objects
            scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]  # Confidence of detected objects

            detection_list.clear()
            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if (scores[i] > min_conf_threshold) and (scores[i] <= 1.0) and (labels[int(classes[i])] =='person' or labels[int(classes[i])] == 'Person'):

                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image
                    # dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1, (boxes[i][0] * imH)))
                    xmin = int(max(1, (boxes[i][1] * imW)))
                    ymax = int(min(imH, (boxes[i][2] * imH)))
                    xmax = int(min(imW, (boxes[i][3] * imW)))
                    
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 255, 0), 2)

                    ## Draw label
                    object_name = labels[int(classes[i])]  # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                    label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
                    cv2.rectangle(frame, (xmin, label_ymin-labelSize[1] - 10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)  # Draw white box to put label text in
                    cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)  # Draw label text

                    # Draw circle in center of object
                    xcenter = xmin + (int(round((xmax - xmin) / 2)))
                    ycenter = ymin + (int(round((ymax - ymin) / 2)))
                    cv2.circle(frame, (xcenter, ycenter), 5, (255, 255, 0), thickness=-1)
                    detection_list.append(object(xcenter, ycenter, xmin, xmax, ymin, ymax))
                    
            # Draw framerate in corner of frame
            #  cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            
            
            for i in detection_list:
                if object_to_follow.distance(i) < min_distance and i.xcenter >= object_to_follow.xmin  and i.xcenter <= object_to_follow.xmax  and i.ycenter >= object_to_follow.ymin and i.ycenter <= object_to_follow.ymax:
                    next_object = i
                    min_distance = object_to_follow.distance(i)
            
            
            
            if min_distance != math.inf:
                min_distance = math.inf
                timer=math.inf # zerowanie zegara
                find_flag=True
                object_to_follow = next_object
                cv2.rectangle(frame, (object_to_follow.xmin, object_to_follow.ymin), (object_to_follow.xmax, object_to_follow.ymax), (0, 0, 255), 2)
                cv2.circle(frame, (object_to_follow.xcenter, object_to_follow.ycenter), 5, (0, 0, 255), thickness=-1)
                robot.run(imW, imH, object_to_follow.xcenter, object_to_follow.ycenter, object_to_follow.xmin, object_to_follow.xmax, object_to_follow.ymin, object_to_follow.ymax)
            else:
                if(find_flag==True):
                    timer=time.time() # uruchomienie zegara zgubienia celu
                find_flag=False 
                robot.stop()
            
            # Jesli wykrto obiekt do sledzenia i robot stoi
            if (robot.stopBOOL==True ):
                # Jesli nie uruchomiono timera w stanie stop to go uruchamiamy
                if(timer_zero==math.inf):
                    timer_zero=time.time()
                # Jesli timer odliczajacy czas postoju obiektu przekroczyl 5 sekund. Uruchomione zostaje wykrywanie gestow
                if(time.time()-timer_zero>5):
                    # zmniejszanie obrazka do opszaru tylko i wylacznie czlowieka
                    croped=frame_rgb[object_to_follow.ymin:object_to_follow.ymax , object_to_follow.xmin:object_to_follow.xmax]
                    result,multi_hand_landmarks=Gesture.detect(croped)
                    if(result!=0): #jesli znaleziono rece/reke wyrysowujemy szkielet
                        for hand in multi_hand_landmarks:
                            for landmark in hand.landmark :
                                landmark.x=((landmark.x*(object_to_follow.xmax-object_to_follow.xmin))+(object_to_follow.xmin))/(imW)
                                landmark.y=((landmark.y*(object_to_follow.ymax-object_to_follow.ymin))+(object_to_follow.ymin))/(imH)
                            drawingModule.draw_landmarks(frame,hand,Gesture.handsModule.HAND_CONNECTIONS)
                    if(result==1): #jesli pokazano wlasciwy gest, zaprzestano seldzic obiekt
                        audio.mixer.music.load("/home/pi/Projekt/TrackingRobot/audio/Target_will_no_longer_be_followed.mp3")
                        audio.mixer.music.play()
                        object_to_follow=object(imW / 2,imH / 2,  0, imW, 0, imH)
                        timer_zero=math.inf #zerowanie timera odliczania stopu
                        timer=-math.inf # ustawienie glownego timera na - inf w celu wejscai w stan tylko i wylacznie wykrywania rak
                        delay_timer=time.time() #uruchomienie opoznienia miedzy wkryciem nastepnego celu
            else:
                timer_zero=math.inf #robot sie porusza "zerowanie" zegara 
            
            # if(Main_flaga==False):
            if((object_to_follow.xcenter!=imW / 2) and (object_to_follow.ycenter != imH / 2) and (object_to_follow.xmin != 0) and (object_to_follow.xmax != imW) and (object_to_follow.ymin!=0) and  (object_to_follow.ymax!=imH) ): 
                for osoba in detection_list:
                    if(osoba.xmin != object_to_follow.xmin and osoba.xmax!=object_to_follow.xmax and osoba.ymin!=object_to_follow.ymin and osoba.ymax != object_to_follow.ymax ):
                        if(object_to_follow.ymax<osoba.ymax):
                            if((object_to_follow.xmin<osoba.xmax and osoba.xmax<object_to_follow.xmax )):    
                                Main_flaga=True
                                Colision_person=object(osoba.xcenter, osoba.ycenter, osoba.xmin, osoba.xmax, osoba.ymin, osoba.ymax)
                                Obszar_xmin=osoba.xmin
                                Obszar_xmax=object_to_follow.xmax
                                Obszar_ymin=osoba.ymin
                                Obszar_ymax=osoba.ymax
                                Flaga_lewo=True
                                delay_waiter=0
                              

                            if(object_to_follow.xmin<osoba.xmin and osoba.xmin<object_to_follow.xmax ):
                                Main_flaga=True
                                Colision_person=object(osoba.xcenter, osoba.ycenter, osoba.xmin, osoba.xmax, osoba.ymin, osoba.ymax)
                                Obszar_xmin=object_to_follow.xmin
                                Obszar_xmax=osoba.xmax
                                Obszar_ymin=osoba.ymin
                                Obszar_ymax=osoba.ymax
                                Flaga_prawo=True
                                delay_waiter=0
                               
            count_persons=0
            if(Main_flaga==True):
                for osoba in detection_list:
                   if(Obszar_xmin < osoba.xcenter and osoba.xcenter < Obszar_xmax and Obszar_ymin < osoba.ycenter and osoba.ycenter < Obszar_ymax  ):
                        count_persons+=1
                if(count_persons==1):                   
                    delay_waiter+=1
                    if(Flaga_lewo):
                            for osoba in detection_list:
                                if( Obszar_xmin*0.85 <= osoba.xcenter and osoba.xcenter<= Obszar_xmin):
                                        Flaga_posrednia=False
                                        Main_flaga=False
                                        Colision_person=None
                                        Obszar_xmin=None
                                        Obszar_xmax=None
                                        Obszar_ymin=None
                                        Obszar_ymax=None
                                        Flaga_lewo=False
                                        Flaga_prawo=False
                                        delay_waiter=0
                                        posredni_timer=None

                    if(Flaga_prawo):
                            for osoba in detection_list:
                                if( Obszar_xmax*1.15 <= osoba.xcenter and osoba.xcenter<= Obszar_xmax):
                                        Flaga_posrednia=False
                                        Main_flaga=False
                                        Colision_person=None
                                        Obszar_xmin=None
                                        Obszar_xmax=None
                                        Obszar_ymin=None
                                        Obszar_ymax=None
                                        Flaga_lewo=False
                                        Flaga_prawo=False
                                        delay_waiter=0
                                        posredni_timer=None
                    
                    if(delay_waiter>20):
                        Flaga_posrednia=True
                        delay_waiter=0

                if(count_persons>1):
                    delay_waiter=0
                    for osoba in detection_list:
                        if(Obszar_xmin < osoba.xcenter and osoba.xcenter < Obszar_xmax and Obszar_ymin < osoba.ycenter and osoba.ycenter < Obszar_ymax  ):
                            if((osoba.ymax-osoba.ymin)/(osoba.xmax-osoba.xmin)<2):
                                Flaga_posrednia=True
            
          # Jesli zgubiono cel/ cel nie chce byc sledzony
        
        else:
        
         #  Jesli minal czas opoznienia miedzy celowym zaprzestaniem sledzenia a ponownym sledzeniem/ w przypadku zgubienia warunek ten jest zawsze prawdziwy
            if(time.time()-delay_timer>4.5):
                croped=frame_rgb[0:imH,int(imW/5):int(imW*4/5)]
            
                #Jesli Prawda to uruchomiono timer zgubienia obiektu i czas przeznaczono na ponowne odnalezienie minal  
                if (timer != -math.inf):
                    audio.mixer.music.load("/home/pi/Projekt/TrackingRobot/audio/Target_was_lost.mp3")
                    audio.mixer.music.play()
                    object_to_follow=object(imW / 2,imH / 2,  0, imW, 0, imH)
                    timer=-math.inf #timer na -inf w celu nie uruchamia tego ^ ifa
                result,multi_hand_landmarks=Gesture.detect(croped)
                #jesli znaleziono rece   
                if(result!=0):
                    for hand in multi_hand_landmarks:
                        for landmark in hand.landmark :
                            landmark.x=(landmark.x*(4/5-1/5))+(1/5)
                        drawingModule.draw_landmarks(frame,hand,Gesture.handsModule.HAND_CONNECTIONS)
                    # jesli wykryto prawidlowy gest
                    if(result==1):
                        audio.mixer.music.load("/home/pi/Projekt/TrackingRobot/audio/Target_will_be_followed.mp3")
                        audio.mixer.music.play()
                        timer=math.inf #timer na inf w celu wejscia w tryb wyszukiwania osob
    
    
    ##################################################################################################################
    
    
    else:   
            if(posredni_timer==None):
                posredni_timer=time.time()

            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()

            # Retrieve detection results
            boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0]  # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]  # Class index of detected objects
            scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]  # Confidence of detected objects

            detection_list.clear()
            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if (scores[i] > min_conf_threshold) and (scores[i] <= 1.0) and (labels[int(classes[i])] =='person' or labels[int(classes[i])] == 'Person'):

                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image
                    # dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1, (boxes[i][0] * imH)))
                    xmin = int(max(1, (boxes[i][1] * imW)))
                    ymax = int(min(imH, (boxes[i][2] * imH)))
                    xmax = int(min(imW, (boxes[i][3] * imW)))
                    
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 255, 0), 2)

                    ## Draw label
                    object_name = labels[int(classes[i])]  # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                    label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
                    cv2.rectangle(frame, (xmin, label_ymin-labelSize[1] - 10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)  # Draw white box to put label text in
                    cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)  # Draw label text

                    # Draw circle in center of object
                    xcenter = xmin + (int(round((xmax - xmin) / 2)))
                    ycenter = ymin + (int(round((ymax - ymin) / 2)))
                    cv2.circle(frame, (xcenter, ycenter), 5, (255, 255, 0), thickness=-1)
                    detection_list.append(object(xcenter, ycenter, xmin, xmax, ymin, ymax))

            for osoba in detection_list:
                if(Obszar_xmin < osoba.xcenter and osoba.xcenter < Obszar_xmax and Obszar_ymin < osoba.ycenter and osoba.ycenter < Obszar_ymax  ):
                    for druga_osoba in detection_list:
                        if (druga_osoba.xmin != osoba.xmin and druga_osoba.xmax != osoba.xmax and druga_osoba.ymin != osoba.ymin and druga_osoba.ymax != osoba.ymax):
                            if((osoba.xmin<druga_osoba.xmax and druga_osoba.xmax<osoba.xmax )):
                                Flaga_posrednia=False
                                Main_flaga=False
                                Colision_person=None

                                Obszar_xmin=None
                                Obszar_xmax=None
                                Obszar_ymin=None
                                Obszar_ymax=None
                                Flaga_lewo=False
                                Flaga_prawo=False

                                delay_waiter=0
                                posredni_timer=None
                                

                            if((osoba.xmin<druga_osoba.xmin and druga_osoba.xmin<osoba.xmax )):
                                Flaga_posrednia=False
                                Main_flaga=False
                                Colision_person=None

                                Obszar_xmin=None
                                Obszar_xmax=None
                                Obszar_ymin=None
                                Obszar_ymax=None
                                Flaga_lewo=False
                                Flaga_prawo=False

                                delay_waiter=0
                                posredni_timer=None
            
            if(time.time()-posredni_timer>3.5):
                Flaga_posrednia=False
                Main_flaga=False
                Colision_person=None

                Obszar_xmin=None
                Obszar_xmax=None
                Obszar_ymin=None
                Obszar_ymax=None
                Flaga_lewo=False
                Flaga_prawo=False

                delay_waiter=0

                posredni_timer=None


            
    
    # All the results have been drawn on the frame, so it's time to display it.

    cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow("Robot",frame)

    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1
   
    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break
    

# Clean up
cv2.destroyAllWindows()
videostream.stop()
