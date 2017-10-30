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

def ex5():
    """5.Multiple Sensor Application
         Create a program that
             Trace the line
             Stop, beep the buzzer and flicker warning light when obstacle is detected
             Wait until no object detected on the line.
             Stop on stop line"""

    pca.set_normal_speed(100)
    def detect(l_ir, c_ir, r_ir):

        if bool(l_ir) and (bool(r_ir) is False) is True:
            pca.go_left()
        elif bool(r_ir) and (bool(r_ir) is False) is True:
            pca.go_right()
        elif bool(c_ir) is True:
            pca.go_forward()
        else:
            pca.stop()
        print l_ir, c_ir, r_ir
        time.sleep(0.3)

    count = 0
    state = False
    state_old = False

    while True:
        l_ir = wp.digitalRead(IN['left_IR'])
        c_ir = wp.digitalRead(IN['center_IR'])
        r_ir = wp.digitalRead(IN['right_IR'])

        # detect if obstacle
        dist = ultra.distance()
        print 'Distance(cm):%.2f' % dist

        if dist < 30:
            pca.stop()
            warn()
            continue
        #detect and follow line
        detect(l_ir, c_ir, r_ir)
        print 'left:%d center:%d right:%d ' % (l_ir, c_ir, r_ir)
        """if bool(c_ir) is True:
            state = True
            if (state_old != state):
                count += 1
                if count == 4:
                    pca.stop()
                    break
                state = state_old"""
        print 'Current Speed: ', pca.nSpeed
    pass

if __name__ == "__main__":
    ex5()            