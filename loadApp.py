import cv2
import time
import streamlit as st
import numpy as np
from PIL import ImageGrab
from PIL import Image
import matplotlib.pyplot as plt
from streamlit_cropper import st_cropper

x_topleft = []
x_bottomright = []
y_topleft = []
y_bottomright = []
cropArr = []

FRAME_WINDOW = st.image([])
 
def clearsessState():
    # Delete all the items in Session state
    for key in st.session_state.keys():
        del st.session_state[key]
    mainApp()


@st.cache
def get_available_devices():
    print("cache miss")
    available_devices = []
    inactive_ports = []
    port_num = 0
    while len(inactive_ports) < 5:
        potential_cam = cv2.VideoCapture(port_num)
        if potential_cam.isOpened() == False:
            inactive_ports.append(port_num)
        else:
            # available_devices.append(port_num)
            is_active, _ = potential_cam.read()
            if is_active:
                available_devices.append(port_num)
            else:
                inactive_ports.append(port_num)
        port_num += 1
        potential_cam.release()


    return available_devices

def get_frame(camera_choice):
    # st.session_state.vid = cv2.VideoCapture(camera_choice, cv2.CAP_DSHOW)
    _, frame = st.session_state.vid.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    st.session_state['cap'] = frame

    # st.session_state['cap'] = ImageGrab.grab(bbox=(115, 143, 1069, 1083))
    st.session_state['cap'] = Image.fromarray(frame)

    st.caption("Frame loaded. Proceed to crop tool.")
    FRAME_WINDOW3 = st.image([])

    FRAME_WINDOW3.image(frame)


def mainApp():

    st.header("HDMI Capture")

    options = st.multiselect(
        'Select languages to read',
        ['English', 'Chinese'])

    if 'lang' not in st.session_state:
        st.session_state['lang'] = ""

    if len(options) == 1:
        if options[0] == "Chinese": 
                st.session_state.lang = "Chn"
                #st.write("Chinese selected")
    elif len(options) == 2:
        if options[1] == "Chinese":
                st.session_state.lang = "Chn"
                #st.write("Chinese selected")

    #st.write('You selected:', options)
        
    # print(options)

    available_devices = get_available_devices()
    camera_choice = st.selectbox( 'Select Video Capture Device',    available_devices)
    st.write("You selected camera number", camera_choice)


    if len(available_devices) != 0:
        run = st.checkbox('Run')
        status = st.empty()

        FRAME_WINDOW2 = st.image([])

        if run:
            if 'vid' not in st.session_state:
                st.session_state['vid'] = []


            st.session_state.vid = cv2.VideoCapture(camera_choice, cv2.CAP_DSHOW)
            st.session_state.vid.set(3, 1280)
            st.session_state.vid.set(4, 720)

            if 'cap' not in st.session_state:
                pass
                # status.subheader("Frame Loading...")

                capture_screenshot = st.button("capture screenshot")
                if capture_screenshot:
                    # cv2.destroyAllWindows()
                    get_frame(camera_choice)
                    # status.subheader("Frame loaded. Proceed to crop tool.")



            status.subheader("Video Preview")
            while run:
                # st.write("Video Capture done")
                # vid.set(3, 1920)
                # vid.set(4, 1080)

                _, frame = st.session_state.vid.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW2.image(frame)







            

    

        

