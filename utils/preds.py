# doing the image pre processing and prediction
# 1. loading the libraries
# 2. loading the models
# 3. image preprocessing - load the img, img to array, resize the image, standardise the image
# 4. do the predictions
# 5. get the preds to a dict
# 6. jsonify and send to the report
from flask import Flask, flash, request, redirect, url_for, render_template
import os
import pickle
import PIL
from PIL import Image
import numpy as np
# import pandas as pd
# import sklearn
# from glob import glob
# import tensorflow as tf
# from tensorflow import keras
# import tensorflow as tf
# import tensorflow
import tensorflow as tf
# from tf import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
# Loading the  Models 
disease_pred_model = tf.keras.models.load_model('model\chickens_EfficientNetB7_final.h5')
# open the model using h5 binary file format in keras model .
# in keras i load the model in h5  Binary Data format use to store large amount of data in the form of multidimensional array
# i have use image classifier machine learning  library
def image_prep(file):
    # This is the image_prep function
        # test = load_img(file, target_size = (224,224))
        # open the image file
        test = Image.open(file)
        test = test.resize((224, 224))  # Adjust size as required
        # image data augmentation is a technique that can used to artifically expand the size of the image dataset .
#     image = np.array(image) / 255.0 #This is the cause of the error # Normalize pixel values
        test_img = np.expand_dims(test, axis=0)
        # convert this test images to the Numpy array list using numpy.expand_dims() function 
        # in here i passed two parameters 
        # axis = Position where new axis to be inserted       
        # disease_pred = np.argmax(disease_pred_model.predict(test_img), axis=1)
        disease_pred = disease_pred_model.predict(test_img)
        # I  can use the array list as disease  prediction  using the predict function
        print('disease_pred score :', disease_pred)
        # get the confidence score  
        # A Confidence Score is a number between 0 and 1 that represents the likelihood that the output of a Machine Learning model is correct and will satisfy a user’s request.
        # get the maximum probability value between 0 and 1 then multply by 100% then rounded as 2 decimal points 
        confidence_score = round(disease_pred.max() * 100, 2)
        # get the accuracy score  using get the maximum value and then multiply by 100% and rounded it with 2 decimal points 
        print(confidence_score)
        disease_pred = np.argmax(disease_pred, axis=1)
        # axis =1 argmax identifies the maximum value for the every row 
        # disease_pred = disease_pred_model.predict(test_img)
        #print(disease_pred)
        if disease_pred == 0:
            disease = "Coccidiosis"
        elif disease_pred == 1:
            disease = "Healthy"
        elif disease_pred == 2:
            disease = "New Castle Disease"
        else:
         #disease_pred == 3:
            disease = "Salmonella"
        return str(disease), confidence_score
    # then  i check the  what is the index of array list which one is get the maximum argument .
# finally i got the output return the disease as string value .
# This process named as inference .This process has some steps image preprocessing ,
# Prediction , return the predition result .This is the   CNN inference pipepline .

