import numpy as np
import argparse
import cv2

trafficlight_xml_file = 'traffic_light.xml'
face_xml_file = 'haarcascade_frontalface_default.xml'
trl_1 = 'trl_1.xml'
trl_2 = 'trl_2.xml'

light_cascade = cv2.CascadeClassifier(trafficlight_xml_file)
face_det = cv2.CascadeClassifier(face_xml_file)
trl_1_det = cv2.CascadeClassifier(trl_1)
trl_2_det = cv2.CascadeClassifier(trl_2)


file='tr8.jpg'

img = cv2.imread(file)
gray = cv2.imread(file,0)


lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

lower_green = np.array([50, 50, 120])
upper_green = np.array([70, 255, 255])

lower_red_1 = np.array([170,100,100])
upper_red_1 = np.array([180,255,255])

lower_red_2 = np.array([0,100,100])
upper_red_2 = np.array([10,255,255])



trls = trl_2_det.detectMultiScale(gray, 1.1, 5)
print (trls)
x1=trls[0][0]
y1=trls[0][1]
x2=x1+trls[0][2]
y2=y1
x3=x1
y3=y1+trls[0][3]
x4=x3+trls[0][2]
y4=y3
print (x1,y1,x2,y2,x3,y3,x4,y4)
for (x,y,w,h) in trls:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),3)

pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
pts2 = np.float32([[0, 0], [200, 0], [0, 200], [200, 200]])
M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (200, 200))

hsv = cv2.cvtColor(dst,cv2.COLOR_BGR2HSV)

# Threshold the HSV image to get only blue colors
red_mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
red_mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
red_mask = red_mask_1+red_mask_2
green_mask = cv2.inRange(hsv, lower_green, upper_green)

mask = green_mask + red_mask # +blue_mask
#if np.array_equal(mask, blue_mask):
#    print ("blue")
if np.array_equal(mask, green_mask):
    print ("green")
if np.array_equal(mask, red_mask):
    print ("red")

# Bitwise-AND mask and original image

res = cv2.bitwise_and(dst, dst, mask=mask)


cv2.imshow('image',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
