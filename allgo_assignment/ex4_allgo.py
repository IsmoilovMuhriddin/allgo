<<<<<<< HEAD
from  allgo_utils import PCA9685,ultrasonic,ir_sens
from  allgo_utils import PCA9685,ultrasonic,ir_sens
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

def ex4():
    """4.IR sensor application
        Create a program with TCRT 5000 IR sensor
            1. Go straight until it detect the 2nd black belt
            2. Stop"""
    count=0
    state = False
    state_old=False
    while(count!=2):
        l_ir = wp.digitalRead(IN['left_IR'])
        c_ir = wp.digitalRead(IN['center_IR'])
        r_ir = wp.digitalRead(IN['right_IR'])

        pca.go_forward(speed_cur=70)
        print 'left:%d center:%d right:%d '%(l_ir,c_ir,r_ir)
        if bool(c_ir) is True:
            state = True
            if(state_old != state):
                count += 1
                if count == 2:
                    pca.stop()
                    break
                state = state_old
            time.sleep(0.2)
    pca.stop_extreme()
    pass

if __name__ == "__main__":
    ex4()        
=======
from  allgo_utils import PCA9685,ultrasonic,ir_sens
from  allgo_utils import PCA9685,ultrasonic,ir_sens
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

def ex4():
    """4.IR sensor application
        Create a program with TCRT 5000 IR sensor
            1. Go straight until it detect the 2nd black belt
            2. Stop"""
    count=0
    state = False
    state_old=False
    while(count!=2):
        l_ir = wp.digitalRead(IN['left_IR'])
        c_ir = wp.digitalRead(IN['center_IR'])
        r_ir = wp.digitalRead(IN['right_IR'])

        pca.go_forward(speed_cur=70)
        print 'left:%d center:%d right:%d '%(l_ir,c_ir,r_ir)
        if bool(c_ir) is True:
            state = True
            if(state_old != state):
                count += 1
                if count == 2:
                    pca.stop()
                    break
                state = state_old
            time.sleep(0.2)
    pca.stop_extreme()
    pass

if __name__ == "__main__":
    ex4()        
>>>>>>> 7351c600657040361015d14e8fea3ad085c2c4af
