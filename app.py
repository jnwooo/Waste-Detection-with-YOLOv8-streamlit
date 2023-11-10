# Python In-built packages
from pathlib import Path
import PIL
from io import BytesIO
from collections import Counter
from tempfile import NamedTemporaryFile
import tempfile
import base64

# External packages
import streamlit as st
import cv2
import numpy as np

# Local Modules
import settings
import helper


# Setting page layout
st.set_page_config(
    page_title="AI 생활 폐기물 분류 시스템",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("AI 생활 폐기물 분류 시스템 :star:")
st.write("")

# Sidebar header
st.sidebar.header("Upload trash images or Videos :fire:")

# Model Options
model_type = st.sidebar.radio(
    "Choose Object detection Models", ['YOLOv8m','YOLOv8s'])

# Sidebar slider
confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100


# Selecting Pre-trained YOLO8 Model
if model_type == 'YOLOv8m':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'YOLOv8s':
    model_path = Path(settings.DETECTION_MODEL_S)

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


# Load Pre-trained YOLO8 Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.write("")
                st.write("EX) Default Image :camera:")
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.write("")
                st.write("Default Image :camera:")
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)                
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(default_detected_image_path)
            st.write("")
            st.write("EX) Detected Image :wrench:")
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image, conf=confidence)
                boxes = res[0].boxes
                labels = boxes.cls
                bbox_coordinates = boxes.xyxy
                res_plotted = res[0].plot()[:, :, ::-1]
                st.write("")
                st.write("Detected Image :wrench:")
                st.image(res_plotted, caption='Detected Image', use_column_width=True)
                st.sidebar.markdown("\n")
                st.sidebar.download_button("Download detected image", 
                                           convert_image(PIL.Image.fromarray(res_plotted)), "Detected Image.png", "image/png")
                
                try:
                    col1, col2 = st.columns(2)
                    with col1:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.data)
                    with col2:
                        with st.expander("Detection Objects"):
                            # match real names to detected classes
                            
                            if len(labels) > 0:
                                labels = [settings.real_names[float(l)] for l in labels]
                                c = Counter(labels)
                                for label, count in c.items():
                                    st.write(f"{label} : {count}개")
                            else:
                                st.write("No objects detected!")
                except Exception as ex:
                    st.write("No image is uploaded yet!")   


elif source_radio == settings.VIDEO:
    
    defaulted_video = st.sidebar.selectbox("Choose a video for check the Model", settings.VIDEOS_DICT.keys())
    source_video = st.sidebar.file_uploader("Choose a video...", type=["mp4", "avi", "mov"])
    is_display_tracker = helper.display_tracker_options()

    col1, col2 = st.columns(2)
    detect_button_clicked = st.sidebar.button('Detect button')

    with col1:
        try:
            if source_video is None:
                st.write("")
                st.write("EX) Default video :camera:") 
                with open(settings.VIDEOS_DICT.get(defaulted_video), 'rb') as video_file:
                    video_bytes = video_file.read()
                    if video_bytes:
                        st.video(video_bytes, format='video/MP4')
            else:
                st.write("Uploaded Video :camera:")
                st.video(source_video, format="video/mp4", start_time=0)

                
        except Exception as ex:
            st.error("Error occurred while opening the Video.")
            st.error(ex)

    with col2:
        try:
            if source_video is None:
                if detect_button_clicked:
                    try:
                        st.write("")
                        st.write("EX) Detected Videos :wrench:")
                        vid_cap = cv2.VideoCapture(str(settings.VIDEOS_DICT.get(defaulted_video)))
                        st_frame = st.empty()
                        while vid_cap.isOpened():
                            success, frame = vid_cap.read()
                            if success:
                                helper._display_detected_frames(confidence, model, st_frame, frame, is_display_tracker)
                            else:
                                vid_cap.release()
                                break
                    except Exception as e:
                        st.error("Error loading default video: " + str(e))
            else:
                # st.write("")
                st.write("Detected Videos :wrench:")
                if detect_button_clicked:
                    try:
                        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                            temp_file.write(source_video.read())
                            temp_file_path = temp_file.name

                        vid_cap = cv2.VideoCapture(temp_file_path)
                        st_frame = st.empty()
            
                        while vid_cap.isOpened():
                            success, frame = vid_cap.read()
                            if success:
                                helper._display_detected_frames(confidence, model, st_frame, frame, is_display_tracker)
                            else:
                                vid_cap.release()
                                break
                    except Exception as e:
                        st.error("Error loading uploaded video: " + str(e))
        except Exception as e:
                    st.error("Error loading uploaded video: " + str(e))

else:
    st.error("Please select a valid source type!")
