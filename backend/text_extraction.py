from paddleocr import PaddleOCR,draw_ocr
ocr = PaddleOCR(use_angle_cls=True, lang='en')
import cv2


def extraction_of_text(image):
    img = cv2.imread(image)
    resized_img = cv2.resize(img, (300, 200), interpolation=cv2.INTER_AREA)
    get_text_from_image = ocr.ocr(resized_img, cls=True)
    if get_text_from_image:
        print(get_text_from_image[0][0][1][0].upper())
    
    return get_text_from_image[0][0][1][0].upper()
# extraction_of_text('/home/sanjayvijaykumar/Documents/IMAGE_EMBED_POC/data_set/text_test/samsung-original.PNG')

#    return get_text_from_original, get_text_from_fake 
