import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="# MS AI SCHOOL")

st.write("## View Your Image")
st.write(": 이미지를 올리세요")

st.sidebar.write("## Upload and Download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def fix_image(upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

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
