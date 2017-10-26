import cv2 
import numpy as np
from  allgo_utils import PCA9685,ultrasonic,ir_sens
import wiringpi as wp
import time

ULTRASONIC_TRIG	= 3 # TRIG port is to use as output signal
ULTRASONIC_ECHO = 23 # ECHO port is to use as input signal
pca = PCA9685()
ultra=ultrasonic(ULTRASONIC_TRIG,ULTRASONIC_ECHO)
def ultra_dist():
    dist=ultra.distance()
    print 'distance:' , dist

def main():
    """ test for motor"""
    print 'choose mode'
    mod=int(input())
    if(mod==1):
        sp=int(input('input Speed'))
        pca.go_left(speed_cur=sp)
    elif mod==2:
        sp = int(input('input Speed'))
        pca.go_right(speed_cur=sp, turning_rate=0.75)
    elif mod==3:
        ultra_dist()


if __name__ == "__main__":
    main()

