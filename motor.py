import cv2 
import numpy as np
import Adafruit_PCA9685 as pca
import wiringpi as wp
import time


pwm = pca.PCA9685()

while True:

    pwm.set_pwm(0,0,1000)
    
    time.sleep(1)

    pwm.set_pwm(0,0,100)

    time.sleep(1)
