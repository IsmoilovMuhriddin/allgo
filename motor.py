import cv2 
import numpy as np
from  allgo_utils import PCA9685,ultrasonic,ir_sens
import wiringpi as wp
import time


pca = PCA9685()

def main():
    pca.go_left(speed_cur=50,turning_rate=0.25)



if __name__ == "__main__":
    main()

