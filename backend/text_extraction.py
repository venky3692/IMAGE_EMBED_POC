from paddleocr import PaddleOCR,draw_ocr
ocr = PaddleOCR(use_angle_cls=True, lang='en')


def extraction_of_text(image):
    get_text_from_image = ocr.ocr(image, cls=True)
    if get_text_from_image:
        print(get_text_from_image[0][0][1][0])
    
    return get_text_from_image[0][0][1][0]
#extraction_of_text('/home/venkatesh/IMAGE_EMBED_POC/data_set/original/justdoit.png')

#    return get_text_from_original, get_text_from_fake 
