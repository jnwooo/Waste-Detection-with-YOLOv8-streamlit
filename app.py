import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import cv2  # OpenCV 라이브러리를 가져옵니다.

st.set_page_config(layout="wide", page_title="# MS AI SCHOOL")

st.write("# MS AI SCHOOL 1조 : AI 생활 폐기물 분류 시스템")
st.write(": ## Upload your trash Image :fire:")

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

    # 이미지를 좌우 반전합니다.
    image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # PIL 이미지를 OpenCV 형식으로 변환합니다.
    flipped_image = cv2.flip(image_cv2, 1)  # 이미지를 좌우로 반전시킵니다.
    flipped_image_pil = Image.fromarray(cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB))  # 다시 PIL 형식으로 변환합니다.
    col2.write("Detected Image :wrench (Flipped):")  # 좌우 반전한 이미지를 표시합니다.
    col2.image(flipped_image_pil)

    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download detected image", convert_image(flipped_image_pil), "bbox.png", "image/png")

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
