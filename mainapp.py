import streamlit as st
import loadApp
import cropApp
import livestreamApp

class MultiApp:
    def __init__(self):
        # List of seperate pages/applications
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application/page.
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
        # gui element to select the page/application
        app = st.selectbox(
            'Navigation',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()


# Initialising the app
mainApp = MultiApp()

# Setting the header for the page
st.title("""
    AI4WRD OCR App
""")

# Adding individual pages to the dropdown menu

mainApp.add_app("Load frame", loadApp.mainApp)
mainApp.add_app("Crop", cropApp.mainApp)
mainApp.add_app("OCR Livestream", livestreamApp.mainApp)


mainApp.run()

