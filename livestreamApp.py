import csv
import random
import time
from datetime import datetime

import cv2
import easyocr
import numpy as np
import pandas as pd
import pytesseract
import streamlit as st
# import paho.mqtt.client as mqtt
from PIL import Image
from paho.mqtt import client as mqtt_client
from pytesseract import Output

from processFrame import SiftFlannAlgo
from resizeFrame import resizeFrame


def ocr_tesseract(crop, ):
    '''
    Function to run optical character recognition using tesseract for detection of languages using
    language models specified by the user
    :param crop:
    :return: a string containing the detected text
    '''
    # Load appropriate models depending on language chosen
    if st.session_state['lang'] == "Traditional Chinese":
        custom_config = r'--oem 3 -l eng+chi_tra --psm 6'
    elif st.session_state['lang'] == "Simplified Chinese":
        print("orwel123")
        print("Simplified Chinese")
        custom_config = r'--oem 3 -l eng+chi_sim --psm 6'
    elif st.session_state['lang'] == "":
        custom_config = r'--oem 3 --psm 6'
    # Return the detected output using the specified configuration
    return pytesseract.image_to_data(crop, config=custom_config, output_type=Output.DICT)


def ocr_easyOcr(crop, reader):
    '''
    Function to perform optical character recognition on images using easyOCR using previously initialised
    language models
    :param crop:
    :param reader: a preinitialized easy_ocr reader instance
    :return: a string containing the read text
    '''
    return reader.readtext(crop)


"""
Section for MQTT Functions
"""


def on_connect(rc):
    # Helper function to check if the app is connected to the specified mqtt broker
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt(client_id, broker, port):
    """
    FUnction to connect to mqtt broker using configuration defined by the user
    :param client_id:
    :param broker:
    :param port:
    :return: Mqtt client class
    """
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


@st.cache
def preprocess_images():
    """
    Preprocessing images and crops using the sift algorithm
    :return: None
    """
    st.session_state['siftFlannAlgo'] = SiftFlannAlgo(st.session_state['crop_data_list'], 0)


def mainApp():
    # Adding images and headers to app
    st.sidebar.image("resources/MSF-logo.gif")
    st.sidebar.header("AI4WRD - OCR App")
    st.sidebar.write(
        "Developed and integrated by the MSF4.0 team at Selangor Human Resource Development Centre (SHRDC)")

    # preprocessing images for algorithms
    preprocess_images()
    # Initializing required variables if they are not yet initialised
    if 'cropArr' not in st.session_state:
        st.session_state['cropArr'] = []

    if 'lang' not in st.session_state:
        st.session_state['lang'] = ""

    if 'data' not in st.session_state:
        st.session_state['data'] = []

    if 'd1' not in st.session_state:
        st.session_state['d1'] = {}
    zoom = st.sidebar.slider('Zoom (%)', 100, 500)

    if 'text' not in st.session_state:
        st.session_state['text'] = []

    # Initialize easy ocr models
    if st.session_state['lang'] == "Simplified Chinese":
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)
    elif st.session_state['lang'] == "Traditional Chinese":
        reader = easyocr.Reader(['ch_tra', 'en'], gpu=True)
    elif st.session_state['lang'] == "":
        reader = easyocr.Reader(['en'], gpu=True)
    # skip_frame = True

    # Checkbox for user to interact with if the cropping process is done
    doneCrop = st.checkbox('Done Crop')

    if doneCrop:
        # allow the user which Optical Chracter Recognition Library to user
        ocr_model = st.selectbox(
            'Choose Model',
            ["tesseract", "easy_ocr"])

        # Widget to allow the user to set the cut-off confidence level
        confidence_level = st.number_input(min_value=0.0, max_value=1.0, value=0.7, step=0.05,
                                           label="OCR Confidence Cut-Off")

        # initialising necessary variables
        continuousSave = 0
        counter = 0
        FRAME_WINDOW = st.image([])
        # initialising text in the header
        header = ['Timestamp', 'Screen No', 'Crop ID', 'OCR Data']
        # initialising a text box for use for status later
        status = st.empty()

        """
        CSV section
        """
        # todo change the use of st.write to another function
        # user defines where to save csv
        path_to_save = st.text_input('Path to save', '')
        if path_to_save != '':
            st.write('The current file is saved to: ', path_to_save + ".csv")

        saveallCSV = st.button("Save Previous to csv")
        savecontCSV = st.button("Save Continuous to csv")

        """
        Mqtt Section 
        """
        status_mqtt = st.empty()
        mqtt_address = st.text_input('Mqtt Broker Address', 'broker.emqx.io')
        mqtt_port = st.number_input('Mqtt Port', 1883)
        mqtt_topic = st.text_input('Mqtt topic to publish to', 'ai4wrd_output')
        publish_mqtt = st.button("Publish to Mqtt server")

        client_id = f'python-mqtt-{random.randint(0, 1000)}'

        if publish_mqtt:
            if mqtt_address != "":
                client = connect_mqtt(client_id, mqtt_address, mqtt_port)

        """
        End of mqtt section
        """

        file_saving_status = st.empty()
        continuousSave = 0  # 0 if false
        while True:
            a = time.time()

            # code to get frames
            _, frame = st.session_state['vid'].read()
            if frame is None:
                st.session_state['vid'] = cv2.VideoCapture(st.session_state['camera_choice'], cv2.CAP_DSHOW)
                st.session_state['vid'].set(3, 1280)
                st.session_state['vid'].set(4, 720)

            # preprocess frame and get crops
            # todo: run the right algo depending on data in cropData
            if "previous_crops_length" not in st.session_state:
                st.session_state['previous_crops_length'] = None
            if frame is not None:

                time_pre_screen_detection = time.time()
                # find the screen and crops that best match the current screen
                current_crops, screen_index = st.session_state['siftFlannAlgo'].process_video_frame(frame)
                # measuring time taken to display the frame
                time_after_screen_detection = time.time()
                time_for_screen_detection = time_after_screen_detection - time_pre_screen_detection
                print(f"its taken {time_for_screen_detection} seconds to process the screens")

                print("streaming")

                # convert image color scheme and display image
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW.image(frame)

                # initialise empty streamlit elements for incoming crops
                livecounter = 0
                if len(current_crops) == 0:
                    status.subheader("No crops made.")
                    if st.session_state['previous_crops_length'] is not None:
                        # if there are insufficient streamlit elements
                        if st.session_state['previous_crops_length'] > len(current_crops):
                            # add more empty streamlit elements
                            for i in range(st.session_state['previous_crops_length']):
                                st.session_state['d1'][f"FRAME_WINDOW{i}"].empty()
                                st.session_state['d1'][f"placeholderOCR{i}"].empty()
                else:
                    status.subheader("")
                    # clearing old crops
                    if st.session_state['previous_crops_length'] is not None:
                        if st.session_state['previous_crops_length'] > len(current_crops):
                            print("removing previous data")
                            for i in range(len(current_crops), st.session_state['previous_crops_length']):
                                st.session_state['d1'][f"FRAME_WINDOW{i}"].empty()
                                st.session_state['d1'][f"placeholderOCR{i}"].empty()
                    st.session_state['previous_crops_length'] = len(current_crops)
                    # Adding more st images as needed
                    while counter < len(current_crops):
                        st.session_state['d1'][f"FRAME_WINDOW{counter}"] = st.image([])
                        st.session_state['d1'][f"placeholderOCR{counter}"] = st.empty()
                        counter += 1

                    # initialising variables needed to check performance of app
                    ocr_time = 0.0
                    timeTakenImageRender = 0.0
                    timeTakenRenderText = 0.0

                    # display all crops
                    while livecounter < len(current_crops):
                        leftco = current_crops[livecounter]["left"]
                        widthco = current_crops[livecounter]["width"]
                        topco = current_crops[livecounter]["top"]
                        heightco = current_crops[livecounter]["height"]

                        # resizing crop
                        newcrop = resizeFrame(frame[topco:topco + heightco, leftco:leftco + widthco], zoom, widthco,
                                              heightco)
                        imgcrop = np.array(newcrop)

                        # checking time taken to display image
                        preImageTime = time.time()
                        st.session_state['d1']["FRAME_WINDOW%s" % livecounter].image(imgcrop)
                        postImageTime = time.time()
                        timeTakenImageRender += (postImageTime - preImageTime)

                        # keeping track of old text
                        oldtext = st.session_state['text']

                        st.session_state['text'] = ""

                        # Measuring time taken to perform ocr
                        time_pre_ocr = time.time()
                        if ocr_model == "tesseract":
                            result = ocr_tesseract(imgcrop)
                            for index in range(len(result['text'])):
                                # ensuring that the confidence level is reached before displaying the text
                                if float(result['conf'][index]) >= confidence_level:
                                    st.session_state['text'] += result['text'][index] + " "

                        elif ocr_model == "easy_ocr":
                            result = ocr_easyOcr(imgcrop, reader)
                            for res in result:
                                # ensuring that the confidence level is reached before displaying the text
                                if res[2] >= confidence_level:
                                    st.session_state['text'] += res[1] + " "
                        # ocr time
                        time_post_ocr = time.time()
                        ocr_time += (time_post_ocr - time_pre_ocr)

                        """
                        formatting output 
                        """
                        # formating the ouput string
                        strIDprint = "Crop " + str(livecounter + 1) + ":      " + st.session_state['text']
                        # calculating the time to render the text
                        pre_render_text = time.time()
                        st.session_state['d1']["placeholderOCR%s" % livecounter].write(strIDprint)
                        post_render_text = time.time()
                        timeTakenRenderText += (post_render_text - pre_render_text)

                        # formatting data for csv and mqtt output
                        csvData = [datetime.now(), " Screen: %s" % (screen_index), " Crop ID: %s" % (livecounter + 1),
                                   st.session_state['text']]

                        """
                        Code to save to csv 
                        """
                        st.session_state['data'].append(csvData)
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
                                        writer.writerows(st.session_state['data'])
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
                                    # continuousSave is 0 if csv does not exist
                                    if continuousSave == 0:
                                        # creating the csv file for the first time
                                        with open(path_to_save + ".csv", 'w', encoding='UTF8', newline='') as f:
                                            writer = csv.writer(f)
                                            # write the header
                                            writer.writerow(header)
                                            continuousSave = 1
                                        # appending to created csv file
                                        with open(path_to_save + ".csv", 'a', encoding='UTF8', newline='') as f:
                                            csv.writer(f).writerows(st.session_state['data'])
                                    # if csv already exist
                                    else:
                                        # just append to csv
                                        with open(path_to_save + ".csv", 'a', encoding='UTF8', newline='') as f:
                                            csv.writer(f).writerow(csvData)
                                    file_saving_status.info("Data stream is being appended to csv file")

                                except Exception as e:
                                    print(e)
                                    file_saving_status.error("Error saving file")
                            else:
                                file_saving_status.error("Path not specified")

                        """
                        Code to publish to mqtt
                        """
                        if publish_mqtt:
                            # time.sleep(1)
                            df = pd.DataFrame(csvData)
                            result = client.publish(mqtt_topic + str(screen_index), df.to_csv(index=False))

                            status_mqtt = result[0]
                            if status_mqtt == 0:
                                # printing status of mqtt
                                print(f"Send `{df.to_csv(index=False)}` to topic `{mqtt_topic + str(screen_index)}`")
                            else:
                                print(f"Failed to send message to topic {mqtt_topic}")

                        cv2.waitKey(0)
                        livecounter += 1

                        # printing performance metrics
                        print(f"its taken {timeTakenImageRender} time to render the IMAGE")
                        print(f"its taken {timeTakenRenderText} time to render the TEXT")
                        print(f"its taken {ocr_time} time to perform ocr]")

                        b = time.time()
                        fps = 1 / (b - a)
                        print(f"the fps is: {fps}")
