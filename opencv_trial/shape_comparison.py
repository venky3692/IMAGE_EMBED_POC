import cv2 
import numpy as np

img1 = cv2.imread('shapes.png')
img2 = cv2.imread('shapes.png')

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)   

_, threshold1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY) 
_, threshold2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY) 

contours1, _ = cv2.findContours( 
    threshold1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours2, _ = cv2.findContours( 
    threshold2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

for contour in contours1: 
    cv2.drawContours(img1, [contour], 0, (0, 0, 255), 5)

for contour in contours2:
    cv2.drawContours(img2, [contour], 0, (0, 0, 255), 5)