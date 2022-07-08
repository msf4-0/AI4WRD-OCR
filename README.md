# AI4WRD-OCR
<!-- omit in toc -->
<a href="https://github.com/msf4-0/AI4WRD-OCR/blob/main/LICENSE">
    <img alt="GitHub" src="https://img.shields.io/github/license/msf4-0/AI4WRD-OCR.svg?color=blue">
</a>
<a href="https://github.com/msf4-0/AI4WRD-OCR/issues">
      <img alt="Issues" src="https://img.shields.io/github/issues/msf4-0/AI4WRD-OCR?color=blue" />
</a>
<a href="https://github.com/msf4-0/AI4WRD-OCR/releases">
    <img alt="Releases" src="https://img.shields.io/github/release/msf4-0/AI4WRD-OCR?color=success" />
</a>
<a href="https://github.com/msf4-0/AI4WRD-OCR/releases">
    <img alt="Downloads" src="https://img.shields.io/github/downloads/msf4-0/AI4WRD-OCR/total.svg?color=success" />
</a>
<a href="https://github.com/msf4-0/AI4WRD-OCR/pulls">
    <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/msf4-0/AI4WRD-OCR?color=blue" />
</a>


AI4WRD is an application that performs Data Extraction through Optical Character Recognition from window based applications. Features include:
1. Ability to use both Easy-OCR and Tesseract to perform Optical Character Recognition
2. Ability to crop the video stream to perform OCR on specific sections of the video
3. Ability to recognise specific screens using the Scale Invariant Feature Transform algorithm and associate them with specific sets of crops
4. Ability to save and load crop configurations
5. Output to both CSV and through the MQTT protocol

A more comprehensive introduction to AI4WRD is available at the AI4WRD-OCR Wiki! Portal to [AI4WRD-OCR wiki](https://github.com/msf4-0/AI4WRD-OCR/wiki). 

## Installation Instructions 
### Using Conda
1. Install conda, https://www.anaconda.com/products/distribution make sure to set environment variables
2. Create an environment with python 3.9
3. Install tesseract at https://github.com/UB-Mannheim/tesseract/wiki, install the chinese language models too
4. Set environment variable for tesseract https://tesseract-ocr.github.io/tessdoc/Installation.html
5. Download git https://git-scm.com/download/
6. Open git cli at a folder where you want to install ai4wrd
7. Run ```git clone https://github.com/msf4-0/AI4WRD-OCR```
8. Start the anaconda environment as a cmd and cd to the AI4WRD folder
9. Run ```pip install -r requirements.txt```
10. Run ```pip install torch==1.10.2+cu113 torchvision==0.11.3+cu113 torchaudio===0.10.2+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html```
11. Run ```export PYTHONIOENCODING=utf8``` if on Linux or OSX or ```set PYTHONIOENCODING=utf8``` if on Windows.
12. Run ```streamlit run mainapp.py```

### Using Pipenv
1. Install tesseract at https://github.com/UB-Mannheim/tesseract/wiki, install the chinese language models too
2. Set environment variable for tesseract https://tesseract-ocr.github.io/tessdoc/Installation.html
3. Install python3.9, either manually set the environment variables or tick the "set environment variable" during installation https://www.python.org/downloads/release/python-3913/
4. Download git https://git-scm.com/download/
5. Open git cli at a folder where you want to install ai4wrd 
6. Run ```git clone https://github.com/msf4-0/AI4WRD-OCR```
7. Start cmd as administrator and cd to the folder AI4WRD-OCR
8. Run ```pip install pipenv```
9. Run ```pipenv shell```
10. Run ```pip install -r requirements.txt```
11. Run ```pip install torch==1.10.2+cu113 torchvision==0.11.3+cu113 torchaudio===0.10.2+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html```
12. Run ```export PYTHONIOENCODING=utf8``` if on Linux or OSX or ```set PYTHONIOENCODING=utf8``` if on Windows.
13. Run ```streamlit run mainapp.py```

## Brief User Guide
For a more detailed guide head to the [AI4WRD-OCR wiki](https://github.com/msf4-0/AI4WRD-OCR/wiki). 

### Application startup
Run the application by first activating your environment, then running the following command in a terminal: ```streamlit run mainapp.py```

### Load Frame
![captureScreen1](https://user-images.githubusercontent.com/72961684/177915062-fa9076e2-561d-4cb5-ab7a-9dc66065fbac.png)
1. When starting up the app, you will arrive at the home page, "Load Frame"
2. This page gives you the option to select the videocapture device using a dropdown menu
3. "Language to detect" dropdown menu allows you to define the language that you want to perform OCR on.
4. Check the "Run" checkbox to preview the video capture
5. Click capture screenshot to take a screenshot of the current video
6. Proceed to the crop tool after capturing all required screenshots

### Cropping tool
![cropScreen1](https://user-images.githubusercontent.com/72961684/177915070-c0756106-99c7-4f05-a35c-2098b2b6e883.png)
1. In the "Crop" page, the first frame of the livestream will be visible to you with a box within
2. In the dropdown menu "choose image", you can choose which one of your previous screenshots you would want to specify the crops for
3. Drag the box to crop the section that you would want to perform ocr on
4. The OCR will be performed on these cropped sections on a later page
5. Select the "Save Crop" button to save the crop, saved crops will appear at the bottom of the page 
6. You may continue to add and store more crops
7. The zoom function is available on the sidebar for you to enlarge crops if the text appears to be too small 
8. Note that the OCR accuracy can be affected depending on the size and clarity of your cropped text
9. Proceed to the next page when you have finished cropping for all desired screenshots
10. You may save or load crop configuration using the text box and buttons at the top of the page

### OCR on Livestream
![liveStream](https://user-images.githubusercontent.com/72961684/177915077-95867da8-88cc-4d5e-9adf-a314602e72e4.png)
1. In the "OCR Livestream" page, check the done crop checkbox to begin livestream
2. The livestream from your capture device will be visible at the top of the page
3. The livestream of the cropped sections will also appear below the main livestream
4. The OCR result of the crop is displayed below each crop
5. The "Choose Model" dropdown menu allows you to select the model used for ocr
6. The "OCR Confidence Cut-Off" widget allows you to filter out detected text below the defined threshold 
7. The "Save Continuous to csv" button will allow you to continuously save new OCR data into a csv file
8. The "Save Previous to csv" button allows you to save all the previous OCR data to a csv file
9. The csv file will be saved at the specified path
10. The "Publish to mqtt button" allows you to publish detected data to a mqtt broker on the Address, Port and Topic specified. Note: if there are multiple crops they will be published to different topics based on the topic name you specified according to the format <topic specified\><crop number\>. For instance, if there are 2 crops and the topic specified is ai4wrdOutput, the text from crop 1 will be published to ai4wrdOutput1 and the text from crop 2 will be publishe to ai4wrOutput2
11. Note that the zoom tool is still available for you to enlarge crops

## Licensing
This software is licensed under the GNU GPLv3 LICENSE © Selangor Human Resource Development Centre. 2021. All Rights Reserved. Users that want to modify and distribute versions of AI4WRD and do not wish to conform to obligations to share the source code are free to contact SHRDC for alternative licensing options.

## Contributing
We welcome any and all contributions through pull requests, whether it be bug fixes or new features.

## Citation
streamlit-cropper component: https://github.com/turner-anderson/streamlit-cropper 
<br />
easy-ocr library: https://github.com/JaidedAI/EasyOCR
<br />
tesseract library: https://github.com/tesseract-ocr/tesseract

[//]: # (Previous demo videos, included for posterity)
[//]: # (https://user-images.githubusercontent.com/99723226/154652833-6d167a30-0c73-4be0-9e6b-5a599fe437b6.mp4)
[//]: # (https://user-images.githubusercontent.com/99723226/154652861-25c9a5d2-d991-4075-97f6-338b1e52baa7.mp4)
[//]: # (https://user-images.githubusercontent.com/99723226/154652921-c9522fd2-6df0-4b29-9992-6d93ef3d956a.mp4)




