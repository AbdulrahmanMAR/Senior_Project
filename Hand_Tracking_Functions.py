#Here are the main hand tracking functions, these functions will serve as important parts for the app to work

import mediapipe as MP
import cv2
import numpy as NP

hands = MP.solutions.hands.Hands
#Function that processes an image through model (mediapipe hands in this case) and outputs results as landmark data
def Process_Image(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #Switch image from BGR to RGB
    #Process the image through model and save landmark data result
    Landmarks_Results = model.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Landmarks_Results

#Function that draws landmarks on tracked hands
def Landmark_Drawing(image, Landmarks_Results):
    #Takes an input image and landmarks detected by mediapipe and draws them on hands
    #Only draws landmarks if they are detected, otherwise, don't do anything
    if Landmarks_Results.multi_hand_landmarks is not None:
        for hand_landmarks in Landmarks_Results.multi_hand_landmarks:
            MP.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, MP.solutions.hands.HAND_CONNECTIONS)