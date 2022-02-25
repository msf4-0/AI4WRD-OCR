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
        
  
    
    run = st.checkbox('Run')
    status = st.empty()
    
    #FRAME_WINDOW2 = st.image([])
     

    if run:

        if 'vid' not in st.session_state:
            st.session_state['vid'] = []

        if 'cap' not in st.session_state:
            status.subheader("Frame Loading...")
            st.session_state.vid = cv2.VideoCapture(0)
            # st.write("Video Capture done")
            # vid.set(3, 1920)
            # vid.set(4, 1080)

            st.session_state.vid.set(3, 1280)
            st.session_state.vid.set(4, 720)

            _, frame = st.session_state.vid.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            st.session_state['cap'] = frame
            
            # st.session_state['cap'] = ImageGrab.grab(bbox=(115, 143, 1069, 1083))
            st.session_state['cap'] = Image.fromarray(frame)
            status.subheader("Frame loaded. Proceed to crop tool.")

            

    

        

