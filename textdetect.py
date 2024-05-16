import os
import pytesseract 
from PIL import Image
current_DIR = os.path.dirname(os.path.abspath(__file__))
pytesseract.pytesseract.tesseract_cmd = os.path.join(current_DIR, r'./OCR/tesseract')

def scan_text(image):
    text = pytesseract.image_to_string(image,lang='kor+eng+jpn+chi-sim')
    return text

if __name__ == "__main__":
    img = Image.open('./test1.png')
    print(scan_text(img))
    img = Image.open('./test2.png')
    print(scan_text(img))