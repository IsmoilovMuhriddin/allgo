from  allgo_utils import PCA9685,ultrasonic,ir_sens
import wiringpi as wp
import time

DIR_DISTANCE_ALERT = 20
preMillis = 0

ULTRASONIC_TRIG	= 3 # TRIG port is to use as output signal
ULTRASONIC_ECHO = 23 # ECHO port is to use as input signal
OUT = [5, 0, 1, 2, 3] # 5:front_left_led, 0:front_right_led, 1:rear_right_led, 2:rear_left_led, 3:ultra_trig
IN = [21, 22, 26, 23] # 21:left_IR, 22:center_IR, 26:right_IR, 23:ultra_echo

LOW = 0
HIGH = 1
OUTPUT = wp.OUTPUT
INPUT = wp.INPUT


pca = PCA9685()
ultra = ultrasonic(ULTRASONIC_TRIG,ULTRASONIC_ECHO)
def setup():
    wp.wiringPiSetup()  # Initialize wiringPi to load Raspbarry Pi PIN numbering scheme
    for i in range(len(OUT)):
        wp.pinMode(OUT[i],OUTPUT)
        wp.digitalWrite(OUT[i], LOW)
    for i in range(len(IN)):
        wp.pinMode(IN[i],INPUT)


def ex1():
    """1. DC Motor Application
        Create a program that:  - Turn smoothly"""
    while(True):
        pca.go_left(speed_cur=120,turning_rate=0.65)
        time.sleep(2)
        pca.stop()
        time.sleep(2)
        pca.go_right(speed_cur=120,turning_rate=0.65)
        time.sleep(2)
        pca.stop()
        time.sleep(2)
        pass

    pass

def ex2():
    """2.Ultrasonic sensor application
         Create a program that
            1. Go forward
            2. Stop and flicker warning light when an Object is closer than 30cm"""
    def warn(times=3):
        for i in times:
            wp.digitalWrite(OUT[0], HIGH)
            wp.digitalWrite(OUT[1], HIGH)
            time.sleep(0.2)
            wp.digitalWrite(OUT[0], LOW)
            wp.digitalWrite(OUT[1], LOW)
            time.sleep(0.2)

    pca.stop()
    pca.set_normal_speed(100)
    while True:

        dist = ultra.distance()
        print 'Distance(sm):%.2f'%dist
        if(dist>30):
            pca.go_forward()
        else:
            pca.stop()
            warn()
        time.sleep(0.3)
    pass

def ex3():
    """3.Ultrasonic Sensor Application
         Create a program that Keep the 50cm distance with an object"""
    pass

def ex4():
    """4.IR sensor application
        Create a program with TCRT 5000 IR sensor
            1. Go straight until it detect the 2nd black belt
            2. Stop"""
    pass

def ex5():
    """5.Multiple Sensor Application
         Create a program that
             Trace the line
             Stop, beep the buzzer and flicker warning light when obstacle is detected
             Wait until no object detected on the line.
             Stop on stop line"""
    pass


def main():
    setup()
    while(True):
        print 'Welcome to the Home work assignment'
        print 'Please select exercise to run:\n' \
              '1 - DC Motor Application\n' \
              '2 - Ultrasonic sensor application\n' \
              '3 - Ultrasonic sensor application\n' \
              '4 - IR sensor application\n' \
              '5 - Multiple Sensor Application\n'
        menu=int(input())
        if menu == 1:
            ex1()
        elif menu == 2:
            ex2()
        elif menu == 3:
            ex3()
        elif menu == 4:
            ex4()
        elif menu == 5:
            ex5()

    pass

if __name__ == "__main__":
    main()