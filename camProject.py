import cv2
import numpy as np
import sys
import img2pdf 
from PIL import Image 
import os 

videoCaptureObject = cv2.VideoCapture(0)
result = True

while(result):
    ret,frame = videoCaptureObject.read() 
    #print(ret)
    #print(frame)
    cv2.imshow('Capturing image',frame)
    if(cv2.waitKey(1) & 0xFF == ord('p')):
        cv2.imwrite("NewPicture.jpg",frame)
        result = False
        
videoCaptureObject.release()
cv2.destroyAllWindows()

#reading image back
# img = cv2.imread('NewPicture.jpg')
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cropping code

cropping = True
x_start, y_start, x_end, y_end = 0, 0, 0, 0

image = cv2.imread('NewPicture.jpg')
oriImage = image.copy()

def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping
 
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
 
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
 
    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished
 
        refPoint = [(x_start, y_start), (x_end, y_end)]
 
        if len(refPoint) == 2: #when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped", roi)
            #Saving cropped image
            cv2.imwrite("Cropped.jpg",roi)
            imagePdf = Image.open("Cropped.jpg")
            # converting into chunks using img2pdf 
            pdf_bytes = img2pdf.convert(imagePdf.filename) 
  
            # opening or creating pdf file 
            file = open("image.pdf", "wb") 
            # writing pdf files with chunks 
            file.write(pdf_bytes) 
  
            # closing image file 
            imagePdf.close() 
  
            # closing pdf file 
            file.close() 
            
    if (cv2.waitKey(1) & 0xFF == ord('s')):
        sys.exit(1)

cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)
cropFlag = True
while True:
 
    i = image.copy()
    if(cv2.waitKey(1) & 0xFF == ord('s')):
        cropFlag = False
    if not cropping:
        cv2.imshow("image", image)
 
    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("image", i)
 
    cv2.waitKey(1)
# close all open windows
cv2.destroyAllWindows()