import pytesseract
import cv2

def extraction_of_text(original_image, fake_image):
    get_text_from_original = pytesseract.image_to_string(cv2.imread(original_image))
    get_text_from_fake = pytesseract.image_to_string(cv2.imread(fake_image))
        
    return get_text_from_original, get_text_from_fake 
