import cv2
import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import fitz

import docx2txt

import pandas as pd



IMAGE_EXTENSIONS = {'png', 'jpg', 'tif'}

def do_preprocessing(file):
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    filepath = f'files/{file.filename}'
    text = ''

    # Get text from file, filetype dependent 
    if file_ext in IMAGE_EXTENSIONS:
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE) # requires string
        text = pytesseract.image_to_string(img)

    elif file_ext == 'pdf':
        document = fitz.open(filepath) # requires string
        text = "\n".join(page.get_text() for page in document)

    elif file_ext == 'docx':
        text = docx2txt.process(file) # takes string, or file-like obj
    
    elif file_ext == 'xlsx':
        text = pd.read_excel(file).to_string(index=False) # takes string, bytes, or file-like obj
    
    elif file_ext == 'csv':
        text = pd.read_csv(file).to_string(index=False) # takes string, bytes, or file-like obj
    
    else:
        raise Exception(f"Processing for filetype {file_ext} not yet implemented in preprocessor.py")

    # Convert text to lowercase
    text = text.lower()

    # Then tokenize for use in NLP model (not needed for BERT model)

    return text

