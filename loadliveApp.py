import streamlit as st
import cv2
import json
import time
import numpy as np
from PIL import ImageGrab
from PIL import Image
import matplotlib.pyplot as plt
from streamlit_cropper import st_cropper
import easyocr
# import paho.mqtt.client as mqtt
from PIL import Image, ImageEnhance


# # initialize for the topic on which the msg is received
# recv_topic = ""
# # initialize a recv msg to store the payload received from MQTT
# recv_msg = ""


# #localhost / 127.0.0.1
# host = "localhost"

# def main_cb(client, userdata, msg):
#     # use `global` to change a variable outside of the callback function
#     global recv_topic, recv_msg
#     recv_topic = msg.topic
#     print('In callback, topic:', recv_topic)
#     if recv_topic == "topic/recv_data":
#         recv_msg = json.loads(msg.payload)
#         print('In callback, msg:', recv_msg)
#     else:
#         recv_msg = msg.payload.decode('utf-8')
#         print('In callback, msg:', recv_msg)


# client = mqtt.Client("ocrDashboard")
# client.connect(host, port=1883)
# client.loop_start()

# client.on_message = main_cb


def mainApp():
        if 'vid' not in st.session_state:
            st.session_state['vid'] = []

        # if 'cropArr' not in st.session_state:
        #     st.session_state['cropArr'] = []
    

        # if 'd' not in st.session_state:
        #     st.session_state['d']= {}

        zoom = st.sidebar.slider('Zoom (%)', 100, 500) 
        doneCrop = st.button('Done Crop')
        statusNew = st.empty()

        if doneCrop:
                statusNew.subheader("Video Loading...")

                
                st.session_state.vid = cv2.VideoCapture(0)
                # st.session_state.vid.set(3, 1920)
                # st.session_state.vid.set(4, 1080)
                st.session_state.vid.set(3, 1280)
                st.session_state.vid.set(4, 720)
                # vid.set(3, 1280)
                # vid.set(4, 720)
                skip_frame = True

                statusNew.subheader("Livestream loaded. Proceed to OCR.")


                # client.publish("topic/numData", len(st.session_state.cropArr))

       