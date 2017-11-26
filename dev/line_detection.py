
#Import modules
import picamera
import picamera.array
import time
import cv2
import numpy as np
#Initialize camera
camera = picamera.PiCamera()
camera.resolution = (640,480)
rawCapture = picamera.array.PiRGBArray(camera)
#Let camera warm up
time.sleep(0.1)

#Capture image
camera.capture(rawCapture, format="bgr")
img = rawCapture.array

#Convert to Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Blur image to reduce noise
blurred = cv2.GaussianBlur(gray, (9, 9), 0)

#Perform canny edge-detection
edged = cv2.Canny(blurred, 50, 150)

#Perform hough lines probalistic transform
lines = cv2.HoughLinesP(edged,1,np.pi/180,10,80,1)

#Draw lines on input image
if(lines != None):
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imshow("line detect test", img) 
cv2.waitKey(0)
