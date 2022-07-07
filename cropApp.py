import time
import traceback
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper
from processFrame import CropData
from resizeFrame import resizeFrame
from saveLoad import save_configuration, load_configuration


def mainApp():
    # Titles for the gui
    st.header("Cropping Tool")
    st.sidebar.image("resources/MSF-logo.gif")
    st.sidebar.header("AI4WRD - OCR App")
    st.sidebar.write(
        "Developed and integrated by the MSF4.0 team at Selangor Human Resource Development Centre (SHRDC)")

    # Wigets for user to define real time update, box color and zoom level
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
    zoom = st.sidebar.slider('Zoom (%)', 100, 500)

    # Initialising variables if not already initialised
    if 'd' not in st.session_state:
        st.session_state['d'] = {}

    # Gui elements to allow user to define save and load location
    save_load_location = st.text_input('Indicate path to save or load file', '')
    saveConfiguration = st.button("Save screen and crop configuration")
    loadConfiguration = st.button("Load screen and crop configuration")
    # If load configuration button is clicked, try to load saved and crop configuration
    if loadConfiguration:
        try:
            st.session_state['crop_data_list'] = load_configuration(save_load_location)
        except FileNotFoundError:
            print(traceback.format_exc())

    # Else get crop configuration from existing session state
    # Check if frame list capture exists
    if 'cap' in st.session_state:
        # Check if there are any frames captured
        if len(st.session_state['cap']) > 0:
            # Check if the frames are already loaded
            if 'crop_data_list' not in st.session_state:
                st.session_state['crop_data_list'] = []
                for i in range(len(st.session_state['cap'])):
                    st.session_state['crop_data_list'].append(CropData(st.session_state['cap'][i], i))

    # Check if crop data list exist and then run cropping function
    if 'crop_data_list' in st.session_state:
        if saveConfiguration:
            crop_data_list = st.session_state['crop_data_list']
            save_configuration(save_load_location, crop_data_list)

       # Select image to crop
        index = st.selectbox(
            'Choose Image',
            [str(i) for i in range(len(st.session_state['crop_data_list']))])
        st.image(st.session_state['crop_data_list'][int(index)].frame)
        crop_app_process(realtime_update, box_color, zoom, st.session_state['crop_data_list'][int(index)])


def crop_app_process(realtime_update, box_color, zoom, cropData):
    """

    :param realtime_update: true if user wants realtime updates
    :param box_color: colour of crop box
    :param zoom: zoom level of image
    :param cropData: list of crops and associated data
    :return:
    """
    run = st.checkbox('Run')
    if run:
        # If realtime update show the updated crop image
        if not realtime_update:
            st.write("Double click to save crop")
        return_type = 'box'
        # Convert to pil image
        pil_frame = Image.fromarray(cropData.frame)
        if return_type == 'box':
            rect = st_cropper(
                pil_frame,
                realtime_update=realtime_update,
                box_color=box_color,
                aspect_ratio=None,
                return_type="box"
            )
            # convert image to np array uint8
            raw_image = np.asarray(cropData.frame).astype('uint8')
            # getting the size of the crop
            left, top, width, height = tuple(map(int, rect.values()))

            # resizing crop
            newimg = resizeFrame(raw_image[top:top + height, left:left + width], zoom, width, height)
            st.image(newimg)

    # Gui element to save crop
    saveCrop = st.button("Save Crop")
    placeholder = st.empty()

    crop = None
    counter = 0

    if saveCrop:
        # Save the crop to session state crop data list
        st.session_state['crop_data_list'][cropData.num].crops.append(rect)
        st.write(st.session_state['crop_data_list'][cropData.num].crops)

        placeholder.header("Saved")
        time.sleep(0.5)
        placeholder.empty()

    # if there are one or more crops, display them on the browser window
    if saveCrop | len(st.session_state['crop_data_list'][cropData.num].crops) > 0:
        # continue displaying images until counter reaches the number of crpos
        while counter < len(st.session_state['crop_data_list'][cropData.num].crops):
            leftco = st.session_state['crop_data_list'][cropData.num].crops[counter]["left"]
            widthco = st.session_state['crop_data_list'][cropData.num].crops[counter]["width"]
            topco = st.session_state['crop_data_list'][cropData.num].crops[counter]["top"]
            heightco = st.session_state['crop_data_list'][cropData.num].crops[counter]["height"]
            # convert to np array
            cap_arr = np.array(cropData.frame)
            # resize image according to zoom level
            newcrop = resizeFrame(cap_arr[topco:topco + heightco, leftco:leftco + widthco], zoom, widthco, heightco)
            # Display images in existing st.session_state
            st.session_state['d']["FRAME_WINDOW%s" % counter] = st.image(newcrop)
            counter += 1
