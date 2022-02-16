import streamlit as st
import loadApp
import loadliveApp
import cropApp
import livestreamApp

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })



    def run(self):
        # app = st.sidebar.radio(
        app = st.selectbox(
            'Navigation',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()


mainApp = MultiApp()

st.title("""
    AI4WRD OCR App

""")


mainApp.add_app("Load frame", loadApp.clearsessState)
mainApp.add_app("Crop", cropApp.mainApp)
mainApp.add_app("Load Livestream", loadliveApp.mainApp)
mainApp.add_app("OCR Livestream", livestreamApp.mainApp)


mainApp.run()

# def form_callback():
#     st.write(st.session_state.my_slider)
#     st.write(st.session_state.my_checkbox)


# with st.form(key='my_form'):
#     slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
#     checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
#     submit_button = st.form_submit_button(label='Submit', on_click=form_callback)