import pytesseract

from PIL import Image

image = Image.open('test_file.jpeg')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

data = pytesseract.image_to_string(image, lang='eng')
print(data)