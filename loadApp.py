import cv2
import streamlit as st


def clearsessState():
    # # Delete all the items in Session state
    for key in st.session_state['keys']():
        del st.session_state[key]
    mainApp()


@st.cache
def get_available_devices():
    """
    function to iterate through video capture ports and return a list
    of ports that are active
    :return: list of active ports
    """
    print("cache miss")
    available_devices = []
    inactive_ports = []
    port_num = 0
    # iterate until 5 inactive ports are found, this is because
    # active ports might not be in sequential order
    while len(inactive_ports) < 5:
        potential_cam = cv2.VideoCapture(port_num)
        # check if the port is active
        if not potential_cam.isOpened():
            inactive_ports.append(port_num)
        else:
            is_active, _ = potential_cam.read()
            if is_active:
                available_devices.append(port_num)
            else:
                inactive_ports.append(port_num)
        port_num += 1
        potential_cam.release()
    return available_devices


def save_frame(frame):
    """
    function to capture a frame from the streamed video and save it to session state
    :param frame: frame of the video
    :return: None
    """
    st.session_state['cap'].append(frame)
    st.caption("Frame loaded.")
    for i in range(len(st.session_state['cap'])):
        st.image(st.session_state['cap'][i], caption=f'Frame number {i}')


def mainApp():
    # setting up the headers and the logo
    st.header("HDMI Capture")
    st.sidebar.image("resources/MSF-logo.gif")
    st.sidebar.header("AI4WRD - OCR App")
    st.sidebar.write(
        "Developed and integrated by the MSF4.0 team at Selangor Human Resource Development Centre (SHRDC)")

    """
    Global Components
    initialising state components if they do not exist
    """
    if 'lang' not in st.session_state:
        st.session_state['lang'] = ""
    if 'cap' not in st.session_state:
        st.session_state['cap'] = []
    if 'vid' not in st.session_state:
        st.session_state['vid'] = []

    # Gui select box for the user to select the language model to use
    st.session_state['lang'] = st.selectbox(
        'Option to try to detect another language',
        ['', 'Traditional Chinese', 'Simplified Chinese'])

    # Get available devices and allow the user to select them using a drop-down menu
    available_devices = get_available_devices()
    camera_choice = st.selectbox('Select Video Capture Device', available_devices)
    st.write("You selected camera number", camera_choice)

    # Only run if there are available devices to stream from
    if len(available_devices) != 0:
        run = st.checkbox('Run')
        status = st.empty()
        # Get the first frame from the video stream
        frame_window2 = st.image([])
        # if user ticks the run checkbox
        if run:
            # initialising the video capture variables
            st.session_state['camera_choice'] = camera_choice
            st.session_state['vid'] = cv2.VideoCapture(camera_choice, cv2.CAP_DSHOW)
            st.session_state['vid'].set(3, 1280)
            st.session_state['vid'].set(4, 720)
            # button to capture screenshot
            capture_screenshot = st.button("capture screenshot")
            if capture_screenshot:
                if "frame" in st.session_state:
                    save_frame(st.session_state["frame"])

            status.subheader("Video Preview")
            while run:
                # loop to capture video frame and display it on screen
                _, st.session_state['frame'] = st.session_state['vid'].read()
                st.session_state['frame'] = cv2.cvtColor(st.session_state["frame"], cv2.COLOR_BGR2RGB)
                frame_window2.image(st.session_state["frame"])
