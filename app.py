import streamlit as st
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(layout="wide", page_title="# MS AI SCHOOL")

st.write("## MS AI SCHOOL : AI 생활 폐기물 분류 시스템")
st.write(": Upload your trash Image :fire:")

st.sidebar.write("## Upload and Download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Download the detected image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def fix_image(upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    col2.write("detected Image :wrench:")
    col2.image(image)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download detected image", convert_image(image), "bbox.png", "image/png")


col1, col2 = st.columns(2)

my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        fix_image(upload=my_upload)
else:
    st.sidebar.markdown("\n")
    st.sidebar.write("No image uploaded.")
