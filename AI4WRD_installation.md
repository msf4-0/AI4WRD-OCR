# Windows Installation

1. Install tesseract at https://github.com/UB-Mannheim/tesseract/wiki, install chinese language models too
2. Set enviroment variable for tesseract https://tesseract-ocr.github.io/tessdoc/Installation.html
3. Install python3.9, make sure to tick "set enviroment variable" box https://www.python.org/downloads/release/python-3913/
4. Download git https://git-scm.com/download/win
5. Open git cli at a folder where you want to install ai4wrd 
6. Run git clone https://github.com/msf4-0/AI4WRD-OCR
7. Start cmd as administrator and cd to the folder AI4WRD-OCR
8. Run pip install pipenv
9. Run pipenv shell
10. Run pip install -r requirements.txt
11. Run pip install torch==1.10.2+cu113 torchvision==0.11.3+cu113 torchaudio===0.10.2+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
12. Run streamlit run mainapp.py
13. Run export PYTHONIOENCODING=utf8