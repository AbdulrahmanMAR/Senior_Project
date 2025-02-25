#Here will be the dataset processing, the program will take an image dataset and turn it into numpy data that will be used to train the model

import os
import mediapipe as MP
import cv2
import numpy as NP
import pickle

from Hand_Tracking_Functions import *

#Dataset directory
dataset_dir = r'C:\Users\yaya2\PycharmProjects\Final Project\Dataset'

#initialize data and label lists
data = []
labels = []

#Defining model parameters
HANDS = MP.solutions.hands.Hands(static_image_mode=True, max_num_hands=2, model_complexity=1, min_detection_confidence = 0.3)

#Goes through each directory in the dataset
for dir_ in os.listdir(dataset_dir): #Using an int so that the data is loaded in correct order
    print(dir_)
    #image number in letter dataset directory
    imnum = 0
    #Takes each image in the letter directory
    for image_path in os.listdir(os.path.join(dataset_dir, str(dir_))):
        DataAux = [] #list for saving x and y before saving it to data list
        X_ = []
        Y_ = []

        imnum += 1
        #reads the image
        image = cv2.imread(os.path.join(dataset_dir, str(dir_), image_path))
        p_results = Process_Image(image, HANDS) #Prcoess the image

        #keypoint extraction loops
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

            data.append(DataAux)
            labels.append(dir_)
    print('has ' + str(imnum) + ' images')

f = (open('data.pickle', 'wb'))
pickle.dump({'data': data, 'labels': labels}, f) #save data with labels to pickle file
f.close()