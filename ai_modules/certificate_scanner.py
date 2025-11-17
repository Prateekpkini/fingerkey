import pytesseract
import cv2
import re

def extract_blood_group(cert_path):
    img = cv2.imread(cert_path)
    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    match = re.search(r'\b(A|B|AB|O)[+-]\b', text)
    return match.group() if match else None
