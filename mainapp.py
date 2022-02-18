import streamlit as st
import loadApp
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
mainApp.add_app("OCR Livestream", livestreamApp.mainApp)


mainApp.run()

