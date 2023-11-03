# Python In-built packages
from pathlib import Path
import PIL
from io import BytesIO

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
st.title("## AI 생활 폐기물 분류 시스템 :star:")

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
                st.write("EX) Original Image :camera:")
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.write("Original Image :camera:")
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)                
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.write("EX) Detected Image :wrench:")
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)            
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image, conf=confidence)
                boxes = res[0].boxes
                if len(boxes) == 0:
                    st.error("No objects detected in the image.")
                else:
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.write("EX) Detected Image :wrench:")
                    st.image(res_plotted, caption='Detected Image',
                            use_column_width=True) 
                    st.sidebar.markdown("\n")
                    st.sidebar.download_button("Download detected image", convert_image(res_plotted), "Detected Image.png", "image/png")
                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.data)
                    except Exception as ex:
                        st.write("No image is uploaded yet!")


elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type!")
