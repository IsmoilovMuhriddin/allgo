from  allgo_utils import PCA9685,ultrasonic,ir_sens
<<<<<<< HEAD
=======
from  allgo_utils import PCA9685,ultrasonic,ir_sens
>>>>>>> 7351c600657040361015d14e8fea3ad085c2c4af
import wiringpi as wp
import time

DIR_DISTANCE_ALERT = 20
preMillis = 0

ULTRASONIC_TRIG	= 3 # TRIG port is to use as output signal
ULTRASONIC_ECHO = 23 # ECHO port is to use as input signal
OUT = {'front_left_led':5,
       'front_right_led':0,
       'rear_right_led':1,
       'rear_left_led':2,
       'ultra_trig':3} # 5:front_left_led, 0:front_right_led, 1:rear_right_led, 2:rear_left_led, 3:ultra_trig
IN = {'left_IR':21,
      'center_IR':22,
      'right_IR':26,
      'ultra_echo':23} # 21:left_IR, 22:center_IR, 26:right_IR, 23:ultra_echo


LOW = 0
HIGH = 1
OUTPUT = wp.OUTPUT
INPUT = wp.INPUT


pca = PCA9685()
ultra = ultrasonic(ULTRASONIC_TRIG,ULTRASONIC_ECHO)
def setup():
    wp.wiringPiSetup()  # Initialize wiringPi to load Raspbarry Pi PIN numbering scheme
    for key in OUT:
        wp.pinMode(OUT[key],OUTPUT)
        wp.digitalWrite(OUT[key], LOW)
    for key in IN:
        wp.pinMode(IN[key],INPUT)
def warn(times=3):
    for i in range(times):
        wp.digitalWrite(OUT['front_right_led'], HIGH)
        wp.digitalWrite(OUT['front_left_led'], HIGH)

        wp.digitalWrite(OUT['rear_right_led'], HIGH)
        wp.digitalWrite(OUT['rear_left_led'], HIGH)
        time.sleep(0.15)

        wp.digitalWrite(OUT['front_right_led'], LOW)
        wp.digitalWrite(OUT['front_left_led'], LOW)

        wp.digitalWrite(OUT['rear_right_led'], LOW)
        wp.digitalWrite(OUT['rear_left_led'], LOW)
        time.sleep(0.15)

def ex2():
    """2.Ultrasonic sensor application
         Create a program that
            1. Go forward
            2. Stop and flicker warning light when an Object is closer than 30cm"""


    pca.stop()
    pca.set_normal_speed(80)
    while True:

        dist = ultra.distance()

<<<<<<< HEAD
        #tprint 'Distance(cm):%.2f' % dist
=======
        print 'Distance(cm):%.2f'%dist
>>>>>>> 7351c600657040361015d14e8fea3ad085c2c4af
        if dist>45:
            pca.set_normal_speed(120)
            pca.go_forward()
        elif dist>40:
            pca.set_normal_speed(70)
            pca.go_forward()
        elif dist>30:
            pca.set_normal_speed(60)
            pca.go_forward()
        elif dist<30:
            pca.stop()
            warn()
        #time.sleep(0.001)
    pass

if __name__ == "__main__":
    ex2()        
