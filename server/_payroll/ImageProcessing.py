import pytesseract
from PIL import Image

# OCR processing
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

# Example usage
extracted_text = extract_text_from_image('timesheet_image.jpg')
print(extracted_text)
