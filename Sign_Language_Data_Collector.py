#Here will be the dataset processing, the program will take an image dataset and turn it into numpy data that will be used to train the model

import os
import mediapipe as MP
import cv2
import numpy as NP
from Hand_Tracking_Functions import *

#Dataset directory
dataset_dir = r'C:\Users\yaya2\PycharmProjects\Final Project\Dataset Cropped'

#Defining what signs will be stored in the data, this will be used for naming the data
signs = NP.array(["أ", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط", "ظ",
                  "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "ه", "و", "ي", "ة", "لا", "ال"])
sign_index = 0

#Defining model parameters
HANDS = MP.solutions.hands.Hands(static_image_mode=True, max_num_hands=2, model_complexity=1, min_detection_confidence = 0.3)

#Data directory name
Data_Dir = "data"

#Goes through each directory in the dataset
for dir_ in range(len(os.listdir(dataset_dir))): #Using an int so that the data is loaded in correct order
    print(dir_)
    #Makes a directory for each letter to store numpy data files
    os.mkdir(os.path.join(Data_Dir, signs[sign_index]))
    #image number in letter dataset directory
    imnum = 0
    #Takes each image in the letter directory
    for image_path in os.listdir(os.path.join(dataset_dir, str(dir_))):
        #reads the image
        image = cv2.imread(os.path.join(dataset_dir, str(dir_), image_path))
        #We have to resize images so that the model can actually learn on consistent data
        if sign_index == 18: #In the dataset we have one letter that uses a different aspect ratio (5:3 instead of 3:5) so that we can capture the letter
            #Note: I'll probably add another letter in 5:3 aspect ratio that doesn't have its data fully captured, we'll see after the training
            resized = cv2.resize(image, (500, 300))
        else:
            resized = cv2.resize(image, (300, 500)) #Most of the dataset is cropped in 3:5
        p_results = Process_Image(resized, HANDS) #Prcoess the image
        keypoints = Extract_Keypoints(p_results) #Extract keypoints
        if len(keypoints) != 0: #check if keypoints were even extracted so that we don't save empty numpy files
            data_path = os.path.join(Data_Dir, signs[sign_index], image_path) #Path to save the numpy data in
            NP.save(data_path, keypoints) #Save numpy data files
            imnum += 1 #next image number
    print(signs[sign_index] + ": has " + str(imnum) + " data files.") #Print how many numpy files were saved for each letter

    sign_index += 1 #next letter directory