import cv2 
import numpy as np
import rasp_car_PCA9685 as pca
import wiringpi as wp
import time


pwm = pca.PCA9685()

while True:

    pwm.go_left()
    
    time.sleep(1)

    pwm.go_right()

    time.sleep(1)
