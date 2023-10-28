# from utils.preds_classifiers import image_prep
from utils.preds import image_prep
from utils import db_models
from utils.database import engine, SessionLocal
from sqlalchemy.orm import Session
from multiprocessing import allow_connection_pickling
from re import template
from tkinter.tix import Form
from urllib.request import Request
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi import FastAPI, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
import os
from pathlib import Path
from fastapi.responses import FileResponse
from random import randint
import uuid
import uvicorn # ASGI 
from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
# classifier related libraries
import os
# import pickle
import PIL
# from PIL import Image
import numpy as np
# import pandas as pd
# import sklearn
# from glob import glob
# import tensorflow as tf
# from tensorflow import keras
# import tensorflow as tf
# import tensorflow
# import tensorflow as tf
# from tf import keras
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
# import cv2
IMAGEDIR_in = 'assets\input'
#IMAGEDIR_out = "assets/output/"
#  Create a FastAPI Application
app = FastAPI()
# connect the model to the  UI through  fast api
# Define the app use the flask framework for web application development 
# fast api is a speedy and lightweight web framework 
# router = APIRouter()
# app.mount("\static", StaticFiles(directory=Path(__file__).parent.parent.absolute()/"static"), name="static",)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets/input", StaticFiles(directory="assets/input"), name="assets")
# Database Function
# Here i use the SQLAlchemy Session using Pip Install SQLAlchemy
# Yield means Return Statement 
# I have Used SQLAlchemy  Session.Get Session local in Fast Api.Return Statement Yeild Method.
# Return Instead of Yield
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()    
        # Database Close       
        # Here I import jinja 2 Templates  using Pip install jinja 2 Command
        # Declare a Request Parameter in the Path Operation that  will Return a Template.
templates = Jinja2Templates(directory='templates')
# index route
# the uvicorn server uses this app object to Listen to the Client's Requests
# using the route render the index.html page 
@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse('index.html', {'request': request})
# trigger  with  index file  submit button 
# Before that Install python multipart Library : This is for uplaoded files are sent as "Form-data" using get or post method.
# using this post request can send images from the Image File .
@app.post("/submit")
# async function used to read the file content and return 
# i send the form data using async function and using request parameters 
# send the Name , Address , Poultry Category , Breeding Type Parameters using async function.Give the response to the api request 
async def get_damage_detection(request:Request, name: str = Form(...), address: str = Form(...),  poultry_breeding_type: str = Form(...), poultry_animal_category: int = Form(...), file : UploadFile = File(...),  db: Session = Depends(get_db)): # request:Request,
    # print(assignment)
    # content = await assignment_file.read()
    # print(content)
    # file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()  # <-- Important!
    file_save_path = os.path.join(IMAGEDIR_in, file.filename)
    # example of how you can save the file
    with open(f"{file_save_path}", "wb") as f:
        f.write(contents)
    # print(file_save_path)
    #  Classification model predictions 
    # Run the image_prep function to get the classfication result and accuracy score 
    classification_result,confidence_score = image_prep(file_save_path)
    # database connectivity adding data    
    db_cases = db_models.Cases()
    db_images = db_models.Images()
    # machine learning part 
    db_predictors = db_models.Predictions()
    # get the last case ID assing the new IDs
    data_reads =  db.query(db_models.Cases).all()
    last_id = data_reads[-1].Case_Id
    print('from the post method: ',last_id)
    new_id = int(last_id) + 1
    # get the last row id and create the new case id 
    # using the  db models class cases
    db_cases.Case_Id = new_id
    db_cases.Name = name
    db_cases.Address = address
    db_cases.Farm_Type = poultry_breeding_type
    db_cases.Animal_Cat = poultry_animal_category
    db_images.Image_Id = new_id 
    db_images.Image_Name = file.filename
    db_images.Image_Loc = file_save_path
    db_predictors.Pred_Id = new_id
    db_predictors.Image_Id = new_id
    db_predictors.Case_Id = new_id
    # Here i  have Called the Predictons  Class  Prediction  String Varible to Get the Classification   Results
    db_predictors.Prediction = classification_result
    # Here i  Called the Predictions Class   Confidence Score String Varible to Get the Confidence Score 
    db_predictors.Confidence_Score = confidence_score
    # Add  Prediction  Results to the  Database 
    # Use the   Library 
    db.add(db_cases)
    db.add(db_images)
    db.add(db_predictors)
    db.commit()
# #printing results ----------------------
#     print('--------------------------------------------------------')
#     print('name: ', name)
#     print('address: ',address)
#     print('poultry_animal_category: ', poultry_animal_category)
#     print('poultry_breeding_type : ', poultry_breeding_type)
# Print Classification Result 
    if classification_result == 'New Castle Disease':
        # return templates.TemplateResponse("portfolio-details.html", {"request": request, 'path': file_save_path})  {"request": request, 'path': file_save_path,'disease': classification_result}
        return templates.TemplateResponse("ncd.html", {"request": request,'path': file_save_path,'disease': classification_result, 'confidence_score': confidence_score})
    elif classification_result == 'Coccidiosis':
        return templates.TemplateResponse("coci.html", {"request": request,'path': file_save_path,'disease': classification_result, 'confidence_score': confidence_score})
    elif classification_result == 'Salmonella':
        return templates.TemplateResponse("sald.html", {"request": request,'path': file_save_path,'disease': classification_result, 'confidence_score': confidence_score})
    else:return templates.TemplateResponse("healthy.html", {"request": request,'path': file_save_path,'disease': classification_result, 'confidence_score': confidence_score})
# send feedback  using post method 
# every entry is a case 
@app.post("/feedback")
async def get_damage_detection(request:Request, feedback: str = Form(...) ,db: Session = Depends(get_db)): # request:Request,
    # add data to db
    # database connectivity adding data
    db_feedbacks = db_models.Feedbacks()
    # get the last case ID assing the new IDs
    data_reads =  db.query(db_models.Cases).all()
    last_id = data_reads[-1].Case_Id
    db_feedbacks.Feedback = feedback
    # Case ID is the foriegn key 
    db_feedbacks.Case_Id = last_id
    db.add(db_feedbacks)
    db.commit()
    print(feedback)
    return 'Thank You For Your Feedback!'
# Run the FastAPI Application with Uvicorn
# start the server using uvicorn command
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
    #  This code starts a Uvicorn server that listen on ort 8000 and serves the FAST  api application
# uvicorn main:app --reload

