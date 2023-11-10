from ultralytics import YOLO
import time
import streamlit as st
import cv2
from pytube import YouTube
import torch
import settings

def load_model(model_path):
    model = YOLO(model_path)
    return model

def display_tracker_options():
    pass

def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None):
    # Resize the image to a standard size
    # image = cv2.resize(image, (720, int(720*(9/16))))
    
    # Display object tracking, if specified
    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True)
    else:
        # Predict the objects in the image using the YOLOv8 model
        res = model.predict(image, conf=conf)
    
    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )
    

