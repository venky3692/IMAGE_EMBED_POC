from paddleocr import PaddleOCR,draw_ocr
ocr = PaddleOCR(use_angle_cls=True, lang='en')


def extraction_of_text(original_image, fake_image):
    get_text_from_original = ocr.ocr(original_image, cls=True)
    get_text_from_fake = ocr.ocr(fake_image, cls=True)
        
    return get_text_from_original, get_text_from_fake 
