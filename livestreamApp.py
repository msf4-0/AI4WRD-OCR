import random

import pytesseract
import PIL
import numpy
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

from paho.mqtt import client as mqtt_client
import pandas as pd

from processFrame import SiftFlannAlgo

from pytesseract import Output


def ocr_tesseract(crop):
    '''
    :param crop:
    :return: a string containing the read text
    '''
    custom_config = r'--oem 3 --psm 6'
    return pytesseract.image_to_data(crop, config=custom_config, output_type=Output.DICT)

def ocr_easyOcr(crop, reader):
    '''
    :param crop:
    :param reader: a preinitialized easy_ocr reader instance
    :return: a string containing the read text
    '''
    return reader.readtext(crop)



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


@st.cache
def connect_mqtt(client_id, broker, port):
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

@st.cache
def preprocess_images():
    # change to use the right algorithm depending on the algorithm list

    # # converting from pil to opencv
    # open_cv_images = []
    # for i in range(len(st.session_state['crop_data_list'])):
    #     open_cv_images.append(cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR))

    st.session_state['siftFlannAlgo'] = SiftFlannAlgo(st.session_state['crop_data_list'], 0)
    st.session_state['siftFlannAlgo'].initialize_algorithm_data()

def mainApp():
    # preprocessing images for algorithms
    preprocess_images()
    # removing checks on whether global variables exist
    if 'cropArr' not in st.session_state:
            st.session_state['cropArr'] = []

    if 'lang' not in st.session_state:
        st.session_state['lang'] = ""


    # Initialize the models
    if st.session_state.lang == "Chn":
        reader = easyocr.Reader(['ch_sim','en'], gpu=True)
        #st.write("Reading Chinese")
    elif st.session_state.lang == "":
        reader = easyocr.Reader(['en'], gpu=True)
        #st.write("Not reading chinese")



    skip_frame = True

    if 'data' not in st.session_state:
            st.session_state['data']= []

    if 'd1' not in st.session_state:
            st.session_state['d1']= {}
    zoom = st.sidebar.slider('Zoom (%)', 100, 500)

    if 'text' not in st.session_state:
            st.session_state['text']= []

    doneCrop = st.checkbox('Done Crop')




    if doneCrop:

        ocr_model = st.selectbox(
            'Choose Model',
            ["tesseract", "easy_ocr"])

        confidence_level = st.number_input(min_value=0.0, max_value=1.0, value=0.7, step=0.05, label="OCR Confidence Cut-Off")

        continuousSave = 0
        counter = 0
        FRAME_WINDOW = st.image([])
        header = ['Timestamp','Crop ID', 'OCR Data']

        status = st.empty()

        # todo dont use st.write
        path_to_save = st.text_input('Path to save', '')
        st.write('The current path is', path_to_save)


        saveallCSV = st.button("Save Previous to csv")

        savecontCSV = st.button("Save Continuous to csv")

        """
        Mqtt test 
        """
        status_mqtt = st.empty()
        mqtt_address = st.text_input('Mqtt Broker Address', '')
        mqtt_topic = st.text_input('Mqtt topic to publish to', '')
        publish_mqtt = st.button("Publish to Mqtt server")

        # mqtt test
        broker = 'broker.emqx.io'
        port = 1883
        topic = "test123456"
        client_id = f'python-mqtt-{random.randint(0, 1000)}'
        # username = 'emqx'
        # password = 'public
        #
        if publish_mqtt:
            client = connect_mqtt(client_id, broker, port)


        """
        end of mqtt test
        """



        file_saving_status = st.empty()




        continuousSave = 0
        # someVideo = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        # someVideo.set(3, 1280)
        # someVideo.set(4, 720)

        while True:
            a = time.time()

            # code to get frames
            _, frame = st.session_state.vid.read()
            if frame is None:
                st.session_state.vid = cv2.VideoCapture(st.session_state.camera_choice, cv2.CAP_DSHOW)
                st.session_state.vid.set(3, 1280)
                st.session_state.vid.set(4, 720)

            # _, frame = someVideo.read()

            for key in st.session_state.keys():
                print(key)
                print(type(st.session_state[key]))

            # preprocess frame and get crops
            # todo: run the right algo depending on data in cropData
            if frame is not None:
                current_crops = st.session_state['siftFlannAlgo'].process_video_frame(frame)
                print("streaming")
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW.image(frame)

                livecounter = 0
                if len(current_crops) == 0:
                    status.subheader("No crops made.")
                else:
                    while counter < len(current_crops):
                        st.session_state.d1["FRAME_WINDOW{0}".format(counter)] = st.image([])
                        st.session_state.d1["placeholderOCR{0}".format(counter)] = st.empty()
                        counter += 1
                    while livecounter < len(current_crops):

                        leftco = current_crops[livecounter]["left"]
                        widthco = current_crops[livecounter]["width"]
                        topco = current_crops[livecounter]["top"]
                        heightco = current_crops[livecounter]["height"]

                        # raw_image = np.asarray(frame).astype('uint8')
                        imgcrop = frame[topco:topco+heightco, leftco:leftco+widthco]
                        cropped_img = Image.fromarray(imgcrop)

                        scale_percent = zoom # percent of original size
                        rewidth = int(widthco * scale_percent / 100)
                        reheight = int(heightco * scale_percent / 100)

                        newsize = (rewidth,reheight)
                        newcrop=cropped_img.resize(newsize)
                        imgcrop = np.array(newcrop)

                        print("livestream app size")
                        print(newsize)

                        st.session_state.d1["FRAME_WINDOW%s" % livecounter].image(imgcrop)

                        # # result = reader.readtext(imgcrop)
                        # custom_config = r'--oem 3 --psm 6'
                        oldtext = st.session_state.text

                        st.session_state.text = ""

                        if ocr_model == "tesseract":
                            result = ocr_tesseract(imgcrop)
                            for index in range(len(result['text'])):
                                if result['conf'][index] >= confidence_level:
                                    st.session_state.text += result['text'][index] + " "

                        elif ocr_model == "easy_ocr":
                            result = ocr_easyOcr(imgcrop, reader)
                            for res in result:
                                if res[2] >= confidence_level:
                                    st.session_state.text += res[1] + " "


                        b = time.time()
                        fps = 1/(b-a)
                        print(fps)

                        strIDprint = "Crop " + str(livecounter+1) + ":      " + st.session_state.text


                        """
                        csv stuff
                        """
                        st.session_state.d1["placeholderOCR%s" % livecounter].write(strIDprint)
                        csvData = [datetime.now(), " Crop ID: %s" %(livecounter+1), st.session_state.text]

                        st.session_state.data.append(csvData)
                        if continuousSave == 1:
                            savecontCSV = 1

                        if saveallCSV:
                            if path_to_save != '':
                                try:
                                    with open(path_to_save + ".csv", 'w', encoding='UTF8', newline='') as f:
                                        writer = csv.writer(f)

                                        # write the header
                                        writer.writerow(header)

                                        # write multiple rows
                                        writer.writerows(st.session_state.data)
                                        saveallCSV = False
                                    file_saving_status.success("File Saved!")

                                except Exception as e:
                                    print(e)
                                    file_saving_status.error("Error saving file")
                            else:
                                file_saving_status.error("Path not specified")





                        elif savecontCSV:
                            if path_to_save != '':
                                try:
                                    with open('path_to_save', 'w', encoding='UTF8', newline='') as f:
                                        writer = csv.writer(f)

                                        if continuousSave == 0:
                                            # write the header
                                            writer.writerow(header)

                                        # write multiple rows
                                        writer.writerows(st.session_state.data)

                                    continuousSave = 1
                                    file_saving_status.info("Data stream is being appended to csv file")

                                except Exception as e:
                                    print(e)
                                    file_saving_status.error("Error saving file")
                            else:
                                file_saving_status.error("Path not specified")

                        elif publish_mqtt:
                            msg_count = 0

                            time.sleep(1)
                            msg = f"messages: {msg_count}"

                            df = pd.DataFrame(csvData)

                            result = client.publish(topic, df.to_csv(index=False))

                            # result: [0, 1]
                            status = result[0]
                            if status == 0:
                                print(f"Send `{msg}` to topic `{topic}`")
                            else:
                                print(f"Failed to send message to topic {topic}")
                            msg_count += 1

                        cv2.waitKey(0)
                        livecounter+=1
