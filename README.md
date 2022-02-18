# AI4WRD-OCR
## Installation
* This app is currently only supported on Windows.
* It is advised to install the application on a device with a dedicated graphics card.
    * Current GPU specifications: NVIDEA Quadro P620 GPU

* Installation Guide: In zipped folder above. 

## User Guide
##### Application startup
1. When starting up the app, you will arrive at the home page, "Load Frame". 
2. This page loads the video capture from your video device. 
3. Check the "Run" checkbox to load the video capture.
4. A message will appear when the video is fully loaded. 
5. Proceed to the crop tool.

https://user-images.githubusercontent.com/99723226/154652833-6d167a30-0c73-4be0-9e6b-5a599fe437b6.mp4




##### Cropping tool
1. In the "Crop" page, the first frame of the livestream will be visible to you with a blue box.
2. Drag the blue box to crop text on the visible frame. 
3. The OCR will be performed on these cropped sections on a later page. 
4. Select the "Save Crop" button to save the crop. 
5. Saved crops will appear at the bottom of the page. 
6. You may continue to add and store more crops. 
7. The zoom function is available on the sidebar for you to enlarge crops if the text appears to be too small. 
8. Note that the OCR accuracy can be affected depending on the size and clarity of your cropped text. 
9. Proceed to the next page when you have finished cropping. 

https://user-images.githubusercontent.com/99723226/154652861-25c9a5d2-d991-4075-97f6-338b1e52baa7.mp4



##### OCR on Livestream
1. In the "OCR Livestream" page, check the done crop checkbox to begin livestream.
2. The livestream from your capture device will be visible at the top of the page. 
3. The livestream of the cropped sections will also appear below the main livestream.
4. The OCR result of the crop is displayed below each crop. 
5. The "Save Continuous to csv" button will allow you to continuously save new OCR data into a csv file. 
6. The "Save Previous to csv" button allows you to save all the previous OCR data to a csv file. 
7. The csv file will be saved under the folder in which you saved the Python program files. 
8. Note that the zoom tool is still available for you to enlarge crops. 
9. 
https://user-images.githubusercontent.com/99723226/154652921-c9522fd2-6df0-4b29-9992-6d93ef3d956a.mp4




## Citation
streamlit-cropper component: https://github.com/turner-anderson/streamlit-cropper 





