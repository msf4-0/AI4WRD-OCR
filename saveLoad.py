import pickle
import streamlit as st
from pathlib import Path

""" 
Uses the pickle module to save crop data to be reloaded at a later date
"""


def save_configuration(path, configuration):
    """
    Save configuration to a pickle at the specified path
    :param path: string
    :param configuration: List[CropData]
    :return: None
    """
    path_to_save = Path(path)
    with open(path_to_save, 'wb') as testPickle:
        someFile = st.session_state['crop_data_list']
        pickle.dump(someFile, testPickle)


def load_configuration(path):
    """
    Load configuration from saved pickle file and returns
    a list of CropData
    :param path: string
    :return: List[CropData]
    """
    path_to_load = Path(path)
    if path_to_load.exists():
        with open(path_to_load, 'rb') as testPickle:
            return pickle.load(testPickle)
    else:
        st.text("Path does not exist")
        raise FileNotFoundError
