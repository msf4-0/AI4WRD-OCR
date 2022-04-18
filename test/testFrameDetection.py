import cv2
import numpy as np
from PIL import ImageGrab
from PIL import Image
import matplotlib.pyplot as plt
from streamlit_cropper import st_cropper
import time



def get_image(camera_choice):
    _, frame = cv2.VideoCapture(camera_choice, cv2.CAP_DSHOW).read()
    return frame


def process_image(frame):
    screen_name = 0
    return screen_name;

while True:
    time.sleep(1)
    frame = get_image(0)
    cv2.imshow(frame)
    print(process_image(frame))
