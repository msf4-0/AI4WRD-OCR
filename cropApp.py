import time
import traceback

import numpy as np
import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper

from processFrame import CropData
from saveLoad import save_configuration, load_configuration

x_topleft = []
x_bottomright = []
y_topleft = []
y_bottomright = []
cropArr = []

FRAME_WINDOW = st.image([])
done1 = 0
done2 = 0


# def preProcessFrames():
#     crop_data_list = []
#     for frame in st.session_state['cap']:
#         st.session_state['crop_data_list'].append(CropData([], frame))

def clearsessState():
    # Delete all the items in Session state
    # del st.session_state['vid']
    # del st.session_state['data']
    # del st.session_state['text']
    # del st.session_state['d1']

    mainApp()


def mainApp():
    # if 'crop_data_list' not in st.session_state:
    #     preProcessFrames()



    st.header("Cropping Tool")
    st.sidebar.image("resources/MSF-logo.gif")
    st.sidebar.header("AI4WRD - OCR App")
    st.sidebar.write("Developed and integrated by the MSF4.0 team at Selangor Human Resource Development Centre (SHRDC)")
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')

    # aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["Free", "1:1", "16:9", "4:3", "2:3"])
    # aspect_dict = {
    #     "Free": None,
    #     "1:1": (1, 1),
    #     "16:9": (16, 9),
    #     "4:3": (4, 3),
    #     "2:3": (2, 3)
    # }
    # aspect_ratio = aspect_dict[aspect_choice]

    # return_type_choice = st.sidebar.radio(label="Return type", options=["Rect coords"])
    # return_type_dict = {
    #     "Rect coords": "box"
    # }
    # return_type = return_type_dict[return_type_choice]

    zoom = st.sidebar.slider('Zoom (%)', 100, 500)

    if 'd' not in st.session_state:
        st.session_state['d'] = {}

    # st.title("HDMI Capture")

    # FRAME_WINDOW2 = st.image([])
    # vid = cv2.VideoCapture(0)

    # @st.cache(suppress_st_warning=True)
    # def firstFrame():
    #     # _, frame = camera.read()
    #     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     # FRAME_WINDOW.image(frame)

    #     cap = ImageGrab.grab(bbox=(115, 143, 1069, 1083))
    #     #cap_arr = np.array(cap)
    #     #gray = cv2.cvtColor(cap_arr, cv2.COLOR_RGB2GRAY)
    #     return cap

    # st.image(cap)

    # @st.cache(suppress_st_warning=True)
    # def cropImg():
    #     if not realtime_update:
    #         st.write("Double click to save crop")
    #     if return_type == 'box':
    #         rect = st_cropper(
    #             capimg,
    #             realtime_update=realtime_update,
    #             box_color=box_color,
    #             aspect_ratio=aspect_ratio,
    #             return_type=return_type
    #         )
    #         #raw_image = np.asarray(cap).astype('uint8')
    #         left, top, width, height = tuple(map(int, rect.values()))
    #         st.write(rect) 
    #     return rect
    save_load_location = st.text_input('Indicate path to save or load file', '')
    saveConfiguration = st.button("Save screen and crop configuration")
    loadConfiguration = st.button("Load screen and crop configuration")

    # load crop data list from configuration
    if loadConfiguration:
        try:
            st.session_state['crop_data_list'] = load_configuration(save_load_location)
        except Exception:
            print(traceback.format_exc())


    # else get crop data list from load app
    if 'cap' in st.session_state:
        if len(st.session_state['cap']) > 0:
            if 'crop_data_list' not in st.session_state:
                st.session_state['crop_data_list'] = []
                for i in range(len(st.session_state['cap'])):
                    st.session_state['crop_data_list'].append(CropData(st.session_state['cap'][i], i))

    # only run cropping function if crop data list exists
    if 'crop_data_list' in st.session_state:
        if saveConfiguration:
            crop_data_list = st.session_state['crop_data_list']
            save_configuration(save_load_location, crop_data_list)

        index = st.selectbox(
            'Choose Image',
            [str(i) for i in range(len(st.session_state['crop_data_list']))])
        st.image(st.session_state['crop_data_list'][int(index)].frame)
        crop_app_process(realtime_update, box_color, zoom, st.session_state['crop_data_list'][int(index)])




def crop_app_process(realtime_update, box_color, zoom, cropData):
    # if 'cap' not in st.session_state:
    #     _, frame = vid.read()
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #     st.session_state['cap'] = crop
    #     cap_true = True
    #     # st.session_state['cap'] = ImageGrab.grab(bbox=(115, 143, 1069, 1083))
    #     st.session_state['cap'] = Image.fromarray(crop)

    # _, frame = st.session_state['vid'].read()

    run = st.checkbox('Run')
    if run:
        if not realtime_update:
            st.write("Double click to save crop")
        return_type = 'box'
        pil_frame = Image.fromarray(cropData.frame)
        if return_type == 'box':
            rect = st_cropper(
                pil_frame,
                realtime_update=realtime_update,
                box_color=box_color,
                aspect_ratio=None,
                return_type="box"
            )
            raw_image = np.asarray(cropData.frame).astype('uint8')
            left, top, width, height = tuple(map(int, rect.values()))
            # st.write(rect)
            # masked_image = np.zeros(raw_image.shape, dtype='uint8')
            cropped_img = raw_image[top:top + height, left:left + width]
            cropped_img = Image.fromarray(cropped_img)

            scale_percent = zoom  # percent of original size
            rewidth = int(width * scale_percent / 100)
            reheight = int(height * scale_percent / 100)

            newsize = (rewidth, reheight)
            newimg = cropped_img.resize(newsize)

            st.image(newimg)




    saveCrop = st.button("Save Crop")
    placeholder = st.empty()

    crop = None
    counter = 0
    print("end of function, for now")
    if saveCrop:
        print("in save crop")
        st.session_state['crop_data_list'][cropData.num].crops.append(rect)
        st.write(st.session_state['crop_data_list'][cropData.num].crops)

        placeholder.header("Saved")
        time.sleep(2)
        placeholder.empty()

    if saveCrop | len(st.session_state['crop_data_list'][cropData.num].crops) > 0:
        while counter < len(st.session_state['crop_data_list'][cropData.num].crops):
            leftco = st.session_state['crop_data_list'][cropData.num].crops[counter]["left"]
            widthco = st.session_state['crop_data_list'][cropData.num].crops[counter]["width"]
            topco = st.session_state['crop_data_list'][cropData.num].crops[counter]["top"]
            heightco = st.session_state['crop_data_list'][cropData.num].crops[counter]["height"]


            # st.write(leftco)
            # st.write(widthco)
            # st.write(topco)
            # st.write(heightco)

            cap_arr = np.array(cropData.frame)

            imgcrop = cap_arr[topco:topco + heightco, leftco:leftco + widthco]
            cropped_img = Image.fromarray(imgcrop)

            scale_percent = zoom  # percent of original size
            rewidth = int(widthco * scale_percent / 100)
            reheight = int(heightco * scale_percent / 100)


            newsize = (rewidth, reheight)
            newcrop = cropped_img.resize(newsize)

            st.session_state['d']["FRAME_WINDOW%s" % counter] = st.image(newcrop)

            counter += 1

            # crop = ImageGrab.grab(bbox=(st.session_state['cropArr[counter].left, st.session_state['cropArr'][counter].top, st.session_state['cropArr'][counter].width, st.session_state['cropArr'][counter].height))
