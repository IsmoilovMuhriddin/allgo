import cv2 
import numpy as np
from  allgo_utils import PCA9685,ultrasonic,ir_sens
import wiringpi as wp
import time


pca = PCA9685()

def main():
    """ test for motor"""
    print 'choose mode'
    mod=int(input())
    if(mod==1):
        sp=int(input('input Speed'))
        pca.go_left(speed_cur=sp,turning_rate=0.25)
    elif mod==2:
        sp = int(input('input Speed'))
        pca.go_right(speed_cur=sp, turning_rate=0.75)


if __name__ == "__main__":
    main()

