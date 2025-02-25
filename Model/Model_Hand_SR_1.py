#Model code, here we will train a model on our numpy data using Tensorflow Keras and Sklearn


import os
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

#Path to numpy data directory
data = pickle.load(open(r'C:\Users\yaya2\PycharmProjects\Final Project\data.pickle', 'rb'))

#Sign and label arrays from pickle file
signs = np.asarray(data['data'])
sign_labels = np.asarray(data['labels'])

#Split data into training and testing sets
X_Train, X_Test, Y_Train, Y_Test = train_test_split(signs, sign_labels, test_size = 0.2, shuffle=True, stratify = sign_labels)

#create a model using the RandomForestClassifier and train it on the training data
model = RandomForestClassifier()
model.fit(X_Train, Y_Train)

#do a prediction to make sure that the model works correctly
Y_predict = model.predict(X_Test)
score = accuracy_score(Y_predict, Y_Test)
print('{}% of samples were classified correctly'.format(score * 100))

#save model to pickle file
with open('model.p', 'wb') as f:
    pickle.dump(model, f)