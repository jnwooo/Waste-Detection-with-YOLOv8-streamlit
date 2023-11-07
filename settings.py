from pathlib import Path
import sys

# Get the absolute path of the current file (only works in .py files) - path to this file ./settings.py
file_path = Path(__file__).resolve()

# Get the parent directory of the current file (main file: /yolov8-streamlit)
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there : allows for things like helper.process_license_plate()
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the main folder (basically IMAGES_DIR = ../yolov8-streamlit/'images')
ROOT = root_path.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
WEBCAM = 'Webcam'
YOUTUBE = 'YouTube'

SOURCES_LIST = [IMAGE, VIDEO]

real_names = {
    0 : 'Paper',
    1 : 'Can',
    2 : 'Glass',
    3 : 'Pet',
    4 : 'Plastic',
    5 : 'Vinyl',
    6 : 'Styrofoam',
    7 : 'Battery',
    8 : 'Can(foreign)',
    9 : 'Glass(foreign)',
    10 : 'Pet(foreign)'
}

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'A2C1.png'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'A2C1_detected.jpg'

# Videos config
VIDEO_DIR = ROOT / 'videos'
VIDEO_1_PATH = VIDEO_DIR / '20231101_0747_video_clip1.mp4'
VIDEO_2_PATH = VIDEO_DIR / '20231101_0812_video_clip1.mp4'
VIDEO_3_PATH = VIDEO_DIR / '20231101_0812_video_clip2.mp4'
VIDEO_4_PATH = VIDEO_DIR / '20231101_video1_clip1.mp4'
VIDEO_5_PATH = VIDEO_DIR / '20231102_0525_video_clip1.mp4'
VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH,
    'video_2': VIDEO_2_PATH,
    'video_3': VIDEO_3_PATH,
    'video_4': VIDEO_4_PATH,
    'video_5': VIDEO_5_PATH,
}

# ML Model config
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'best.pt'
DETECTION_MODEL_S = MODEL_DIR / 'best_S.pt'



# Webcam
WEBCAM_PATH = 0
