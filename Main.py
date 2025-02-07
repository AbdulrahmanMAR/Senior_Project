#Esharat - Saudi Sign Language Translator

import numpy as NP
import mediapipe as MP
import cv2
from Hand_Tracking_Functions import *
import os
import keyboard

#Initilazing lists
keypoints = []


#Access camera and check if it's opened
capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print("can't access camera.")
    exit()


#Holistic object for hand tracking/sign prediction with confidence percentages for detection and tracking
with MP.solutions.holistic.Holistic(min_detection_confidence = 0.75, min_tracking_confidence = 0.75) as HLS:
    while capture.isOpened():   #loop while camera is opened
        _, img = capture.read() #read frame and save to variable
        #Process image for landmarks through the "Process_Image" function from Hand_Tracking_Functions
        p_results = Process_Image(img, HLS)
        #Draw landmarks on image for landmarks through the "Landmark_Drawing" function from Hand_Tracking_Functions
        Landmark_Drawing(img, p_results)
        #Extract keypoints from landmarks through the "Extract_Keypoints" function from Hand_Tracking_Functions and add it to "keypoints" list
        keypoints.append(Extract_Keypoints(p_results)) #These keypoints will be used later in the model to predict sign language

        #Show camera on display
        cv2.imshow('Camera', img)
        cv2.waitKey(1)

        #Break loop if Camera is closed
        if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
            break

#Release the camera capture and close all windows
capture.release()
cv2.destroyAllWindows()