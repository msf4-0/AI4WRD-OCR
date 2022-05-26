import cv2
import streamlit as st
from PIL import Image


# x_topleft = []
# x_bottomright = []
# y_topleft = []
# y_bottomright = []
# cropArr = []
#
# FRAME_WINDOW = st.image([])

# @st.cache
def clearsessState():
    # # Delete all the items in Session state
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

    # st.session_state['cap'] = ImageGrab.grab(bbox=(115, 143, 1069, 1083))
    # st.session_state['cap'].append(Image.fromarray(frame))]
    st.session_state['cap'].append(frame)


    st.caption("Frame loaded.")
    for i in range(len(st.session_state['cap'])):
        st.image(st.session_state['cap'][i], caption=f'Frame number {i}')


def mainApp():
    # clearsessState()
    st.header("HDMI Capture")

    st.session_state.lang = st.selectbox(
        'Option to try to detect another language',
        ['', 'Traditional Chinese', 'Simplified Chinese'])

    if 'lang' not in st.session_state:
        st.session_state['lang'] = ""
    #
    # if len(options) > 0:
    #     if "Chinese Simplified" in options:
    #         st.session_state.lang = "Chi_sim"
    #         # st.write("Chinese selected")
    #     elif "Chinese Traditional" in options:
    #         st.session_state.lang = "Chi_tra"
    #             # st.write("Chinese selected")

    # st.write('You selected:', options)

    # print(options)

    available_devices = get_available_devices()
    camera_choice = st.selectbox('Select Video Capture Device', available_devices)
    st.write("You selected camera number", camera_choice)

    """
    global components
    """
    if 'cap' not in st.session_state:
        st.session_state['cap'] = []
    if 'vid' not in st.session_state:
        st.session_state['vid'] = []

    if len(available_devices) != 0:
        run = st.checkbox('Run')
        status = st.empty()

        frame_window2 = st.image([])

        if run:
            st.session_state['camera_choice'] = camera_choice
            st.session_state.vid = cv2.VideoCapture(camera_choice, cv2.CAP_DSHOW)
            st.session_state.vid.set(3, 1280)
            st.session_state.vid.set(4, 720)

            # if 'cap' not in st.session_state:
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
                frame_window2.image(frame)
