#Here are the main hand tracking functions, these functions will serve as important parts for the app to work

import mediapipe as MP
import cv2
import numpy as NP
import numpy as np

hands = MP.solutions.hands.Hands
#Function that processes an image through model (mediapipe holistic in this case) and outputs results as landmark data
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

#Fucntion to extract landmark keypoints as numpy array
def Extract_Keypoints(Landmarks_Results):

    #Initialize NP arrays
    handl_Keypoints = NP.empty((0, 21), int)
    handr_Keypoints = NP.empty((0, 21), int)
    #Initialize hand label (left or right)
    hand_label = str

    #Find the hand label from the results to check which hand is detected
    #This isn't useful when showing both hands as the app focuses on one but does detect both
    #the main use of this will be to concatenate the keypoints correctly during dataset processing
    if Landmarks_Results.multi_handedness is not None:
        for hand in Landmarks_Results.multi_handedness:
            hand_label = hand.classification[0].label

    #Extracting keypoints from hands if present
    if Landmarks_Results.multi_hand_landmarks is not None:
        #Checks if the handlandmarks are for the left hand and extracts the keypoints
        for hand_landmarks in Landmarks_Results.multi_hand_landmarks:
            handl_Keypoints = NP.append(handl_Keypoints, NP.array([[LM.x, LM.y, LM.z] for LM in hand_landmarks.landmark]).flatten()
                if hand_label == "Left" else NP.zeros(63))
        # Checks if the handlandmarks are for the right hand and extracts the keypoints
        for hand_landmarks in Landmarks_Results.multi_hand_landmarks:
            handr_Keypoints = NP.append(handr_Keypoints, NP.array([[LM.x, LM.y, LM.z] for LM in hand_landmarks.landmark]).flatten()
                if hand_label == "Right" else NP.zeros(63))

    #Concatenate left and right hand keypoints
    keypoints = NP.concatenate([handl_Keypoints, handr_Keypoints])

    return keypoints