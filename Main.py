#Esharat - Saudi Sign Language Translator

import numpy as np
import mediapipe as MP
import cv2
from Hand_Tracking_Functions import *
import os
import keyboard
import pickle

#Labels dictionary so the program prints out the correct letter
signs = {0: "أ",1: "ب",2: "ت",3: "ث",4: "ج",5: "ح",6: "خ",7: "د",8: "ذ", 9: "ر",10: "ز",
      11: "س",12: "ش",13: "ص",14: "ض",15: "ط",16: "ظ",17: "ع",18: "غ",19: "ف",20: "ق",
       21: "ك",22: "ل",23: "م",24: "ن",25: "ه",26: "و",27: "ي",28: "ة",29: "لا",30: "ال"}


#Access camera and check if it's opened
capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print("can't access camera.")
    exit()
#Define model
with open(r'C:\Users\yaya2\PycharmProjects\Final Project\Model\model.p', 'rb') as f:
    model = pickle.load(f)

DOIT = 0 #sort of a timer before a letter gets printed
#Holistic object for hand tracking/sign prediction with confidence percentages for detection and tracking
with MP.solutions.hands.Hands(max_num_hands=2, model_complexity=1, min_detection_confidence = 0.3, min_tracking_confidence = 0.3) as HANDS:
    while capture.isOpened():   #loop while camera is opened
        #Initialize lists for data extraction
        DataAux = []
        X_ = []
        Y_ = []

        _, img = capture.read() #read frame and save to variable
        #Process image for landmarks through the "Process_Image" function from Hand_Tracking_Functions
        p_results = Process_Image(img, HANDS)
        #Draw landmarks on image for landmarks through the "Landmark_Drawing" function from Hand_Tracking_Functions
        Landmark_Drawing(img, p_results)

        if p_results.multi_hand_landmarks:
            for hand_landmarks in p_results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    X_.append(x)
                    Y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    DataAux.append(x - min(X_))
                    DataAux.append(y - min(Y_))

            if len(DataAux) == 42 and DOIT == 30:
                prediction = model.predict([np.asarray(DataAux)])
                predicted_character = signs[int(prediction[0])]
                print(predicted_character)
                DOIT = 0
            DOIT += 1

        #Show camera on display
        cv2.imshow('Camera', img)
        cv2.waitKey(1)

        #Break loop if Camera is closed
        if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
            break

#Release the camera capture and close all windows
capture.release()
cv2.destroyAllWindows()