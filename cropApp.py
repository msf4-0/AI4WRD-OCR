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
done1 = 0
done2 = 0 

def clearsessState():
    # Delete all the items in Session state
    del st.session_state['vid']
    del st.session_state['data']
    del st.session_state['text']
    del st.session_state['d1']


    mainApp()
    

def mainApp():

    st.header("Cropping Tool")
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
        st.session_state['d']= {}

    #st.title("HDMI Capture")
    run = st.checkbox('Run')
    
    #FRAME_WINDOW2 = st.image([])
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
        
        
        #st.image(cap)

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



    if run:
        # if 'cap' not in st.session_state:
        #     _, frame = vid.read()
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
        #     st.session_state['cap'] = frame
        #     cap_true = True
        #     # st.session_state['cap'] = ImageGrab.grab(bbox=(115, 143, 1069, 1083))
        #     st.session_state['cap'] = Image.fromarray(frame)


        
        if st.session_state.cap:
            if not realtime_update:
                st.write("Double click to save crop")
            return_type = 'box'
            if return_type == 'box': 
                rect = st_cropper(
                    st.session_state.cap,
                    realtime_update=realtime_update,
                    box_color=box_color,
                    aspect_ratio=None,
                    return_type="box"
                )

            
                raw_image = np.asarray(st.session_state.cap).astype('uint8')
                left, top, width, height = tuple(map(int, rect.values()))
                # st.write(rect)
                # masked_image = np.zeros(raw_image.shape, dtype='uint8')
                cropped_img = raw_image[top:top + height, left:left + width]
                cropped_img = Image.fromarray(cropped_img)
                
                scale_percent = zoom # percent of original size
                rewidth = int(width * scale_percent / 100)
                reheight = int(height * scale_percent / 100)

                newsize = (rewidth,reheight)
                newimg=cropped_img.resize(newsize)
                
                st.image(newimg)
                # st.image(Image.fromarray(masked_image), caption='masked image')



    saveCrop = st.button("Save Crop")
    placeholder = st.empty()

    crop = None
    counter = 0

    if 'cropArr' not in st.session_state:
        st.session_state['cropArr'] = []
    counter = 0

    if saveCrop:
        
        st.session_state.cropArr.append(rect)
        st.write(st.session_state.cropArr)
        
        placeholder.header("Saved")
        time.sleep(2)
        placeholder.empty()
        
        

    if saveCrop | len(st.session_state.cropArr)>0:
        while counter < len(st.session_state.cropArr):
            
            leftco = st.session_state.cropArr[counter]["left"]
            widthco = st.session_state.cropArr[counter]["width"]
            topco = st.session_state.cropArr[counter]["top"]
            heightco = st.session_state.cropArr[counter]["height"]

            # st.write(leftco)
            # st.write(widthco)
            # st.write(topco)
            # st.write(heightco)
            
            cap_arr = np.array(st.session_state.cap) 

            imgcrop = cap_arr[topco:topco+heightco, leftco:leftco+widthco]
            cropped_img = Image.fromarray(imgcrop)
                
            scale_percent = zoom # percent of original size
            rewidth = int(widthco * scale_percent / 100)
            reheight = int(heightco * scale_percent / 100)

            newsize = (rewidth,reheight)
            newcrop=cropped_img.resize(newsize)

            
            st.session_state.d["FRAME_WINDOW%s" % counter ] = st.image(newcrop)
            
            
            counter+=1

        

            #crop = ImageGrab.grab(bbox=(st.session_state.cropArr[counter].left, st.session_state.cropArr[counter].top, st.session_state.cropArr[counter].width, st.session_state.cropArr[counter].height))
            



            
            
