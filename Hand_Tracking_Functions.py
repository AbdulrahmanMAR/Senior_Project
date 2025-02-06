import mediapipe as MP
import cv2
import numpy as NP

#Function that processes an image through model (mediapipe holistic in this case) and outputs results as landmarks
def Process_Image(image, model):
    image.flags.writable = False #Set image to read only mode
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #Switch image from BGR to RGB
    #Process the image through model and save result
    Landmarks_Results = model.process(image)
    image.flags.writable = True #Reset the image to writable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #Reset the image to BGR
    return Landmarks_Results

#Function that draws landmarks on tracked hands
def Landmark_Drawing(image, Landmarks_Results):
    #Takes an input image and landmarks detected by mediapipe and draws them on hands
    #Left Hand
    MP.solutions.drawing_utils.draw_landmarks(image, Landmarks_Results.right_hand_landmarks, MP.solutions.holistic.HAND_CONNECTIONS)
    #Right Hand
    MP.solutions.drawing_utils.draw_landmarks(image, Landmarks_Results.left_hand_landmarks, MP.solutions.holistic.HAND_CONNECTIONS)

#Fucntion to extract landmark keypoints as ndarray
def Extract_Keypoints(Landmarks_Results):
    #Extracting keypoints from right hands if present, set to zero otherwise
    Right_Keypoints = NP.array([[LM.x, LM.y, LM.z] for LM in Landmarks_Results.right_hand_landmarks]).flatten() \
        if Landmarks_Results.right_hand_landmarks else NP.zeros(63)
    # Extracting keypoints from Left hands if present, set to zero otherwise
    Left_Keypoints = NP.array([[LM.x, LM.y, LM.z] for LM in Landmarks_Results.left_hand_landmarks]).flatten() \
        if Landmarks_Results.left_hand_landmarks else NP.zeros(63)
    #Concatenate keypoints
    keypoints = NP.concatenate(Left_Keypoints, Right_Keypoints)
    return keypoints