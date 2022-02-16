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
import csv
from datetime import datetime


def mainApp():
    if 'cropArr' not in st.session_state:
            st.session_state['cropArr'] = []


    reader = easyocr.Reader(['en'], gpu=True)
    skip_frame = True

    if 'data' not in st.session_state:
            st.session_state['data']= []

    if 'd1' not in st.session_state:
            st.session_state['d1']= {}
    zoom = st.sidebar.slider('Zoom (%)', 100, 500)

    if 'text' not in st.session_state:
            st.session_state['text']= []
    
    continuousSave = 0
    counter = 0
    FRAME_WINDOW = st.image([])
    header = ['Timestamp','Crop ID', 'OCR Data']

    status = st.empty()
    saveallCSV = st.button("Save ALL to csv")
    savecontCSV = st.button("Save Continuous to csv")

    while counter < len(st.session_state.cropArr):
        st.session_state.d1["FRAME_WINDOW{0}".format(counter)] = st.image([])
        st.session_state.d1["placeholderOCR{0}".format(counter)] = st.empty()
        counter+=1

    continuousSave = 0
    while True:
        a = time.time()
        _, frame = st.session_state.vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

        livecounter = 0
        if len(st.session_state.cropArr) == 0:
            status.subheader("No crops made.")
        else:
            while livecounter < len(st.session_state.cropArr):

                leftco = st.session_state.cropArr[livecounter]["left"]
                widthco = st.session_state.cropArr[livecounter]["width"]
                topco = st.session_state.cropArr[livecounter]["top"]
                heightco = st.session_state.cropArr[livecounter]["height"]

                imgcrop = frame[topco:topco+heightco, leftco:leftco+widthco]
                cropped_img = Image.fromarray(imgcrop)
                
                scale_percent = zoom # percent of original size
                rewidth = int(widthco * scale_percent / 100)
                reheight = int(heightco * scale_percent / 100)

                newsize = (rewidth,reheight)
                newcrop=cropped_img.resize(newsize)
                imgcrop = np.array(newcrop)

                st.session_state.d1["FRAME_WINDOW%s" % livecounter].image(imgcrop)

                result = reader.readtext(imgcrop)
                
                oldtext = st.session_state.text

                st.session_state.text = ""
                for res in result:
                    st.session_state.text += res[1] + " "

                
                #print(text)

                b = time.time()
                fps = 1/(b-a)    
                print(fps)

                # strIDprint = "Crop %s:" % (livecounter+1)
                # strprint = strIDprint + "       " +st.session_state.text
                # st.session_state.d1["placeholderOCR%s" % livecounter].write(strprint)

                st.session_state.d1["placeholderOCR%s" % livecounter].write(st.session_state.text)
                csvData = [datetime.now(), " Crop ID: %s" %(livecounter+1), st.session_state.text]

                st.session_state.data.append(csvData)

                if saveallCSV:
                    with open('ocrCSVData_all.csv', 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)

                        # write the header
                        writer.writerow(header)

                        # write multiple rows
                        writer.writerows(st.session_state.data)
                        saveallCSV = False

                if continuousSave == 1:
                    savecontCSV = 1

                if savecontCSV:
                    with open('ocrCSVData_cont.csv', 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)

                        if continuousSave == 0:
                            # write the header
                            writer.writerow(header)

                        # write multiple rows
                        writer.writerows(st.session_state.data)
                    
                    continuousSave = 1


                cv2.waitKey(0)
                livecounter+=1  