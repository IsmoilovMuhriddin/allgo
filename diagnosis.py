"""// diagnosis.cpp
#include <wiringPi.h>
#include <stdio.h>
#include "PCA9685.h"
#include "Ultrasonic.h"
#include <signal.h>"""
from multiprocessing import Process
import sys
import Adafruit_PCA9685 as pca
import wiringpi as wp
import signal
import sys
import time
import hcsr04sensor.sensor as uls

LOW = 0
HIGH = 1
OUTPUT = wp.OUTPUT
INPUT = wp.INPUT

CAR_DIR_FW  = 0   
CAR_DIR_BK   = 1   
CAR_DIR_LF  = 2  
CAR_DIR_RF   = 3  
CAR_DIR_ST = 4

DIR_DISTANCE_ALERT = 20
preMillis = 0

keepRunning = 1

OUT = [5, 0, 1, 2, 3] # 5:front_left_led, 0:front_right_led, 1:rear_right_led, 2:rear_left_led, 3:ultra_trig
IN = [21, 22, 26, 23] # 21:left_IR, 22:center_IR, 26:right_IR, 23:ultra_echo

ULTRASONIC_TRIG	= 3 # TRIG port is to use as output signal
ULTRASONIC_ECHO = 23 # ECHO port is to use as input signal 

# An instance of the motor & buzzer
pca9685 =pca.PCA9685()  
#Ultrasonic ultra; # An instance of the ultrasonic sensor
ultra = uls.Measurement(ULTRASONIC_TRIG,ULTRASONIC_ECHO)

# distance range: 2cm ~ 5m
# angular range: 15deg
# resolution: 3mm
"""
void setup();
void loop();
void checkUltra();
void intHandler(int dummy);
"""

def setup():
    wp.wiringPiSetup()  # Initialize wiringPi to load Raspbarry Pi PIN numbering scheme
    
    """
	for(i=0; i<sizeof(OUT); i++){
		pinMode(OUT[i], OUTPUT); // Set the pin as output mode
		wp.digitalWrite(OUT[i], LOW); // Transmit HIGH or LOW value to the pin(5V ~ 0V)
    }"""
    for i in range(len(OUT)):
        wp.pinMode(OUT[i],OUTPUT)
        wp.digitalWrite(OUT[i], LOW)
    for i in range(len(IN)):
        wp.pinMode(IN[i],INPUT)

def check_ultra():
	rawDis=ultra.raw_distance()
	disValue = ultra.distance_metric(rawDis)
	print("Distance:{0}\t Raw dist:{1}",rawDis,disValue)
def action(menu):
   	global curMillis

	if menu==0:
		pca9685.go_forward();
		time.sleep(20);
		pca9685.stop();
		
	elif menu== 1:
		pca9685.go_back();
		time.sleep(20);
		pca9685.stop();
		
	elif menu== 2:
		# frount left
		wp.digitalWrite(OUT[0], HIGH);
		time.sleep(20);
		wp.digitalWrite(OUT[0], LOW);
		time.sleep(20);
		wp.digitalWrite(OUT[0], HIGH);
		time.sleep(20);
		wp.digitalWrite(OUT[0], LOW);
		
	elif menu== 3:
		#// frount right
		wp.digitalWrite(OUT[1], HIGH);
		time.sleep(20);
		wp.digitalWrite(OUT[1], LOW);
		time.sleep(20);
		wp.digitalWrite(OUT[1], HIGH);
		time.sleep(20);
		wp.digitalWrite(OUT[1], LOW);
		
	elif menu== 4:
		#// rear left
		wp.digitalWrite(OUT[3], HIGH);
		time.sleep(20);
		wp.digitalWrite(OUT[3], LOW);
		time.sleep(20);
		wp.digitalWrite(OUT[3], HIGH);
		time.sleep(20);
		wp.digitalWrite(OUT[3], LOW);
		
	elif menu== 5:
		# rear right
		wp.digitalWrite(OUT[2], HIGH);
		time.sleep(20);
		wp.digitalWrite(OUT[2], LOW);
		time.sleep(20);
		wp.digitalWrite(OUT[2], HIGH);
		time.sleep(20);
		wp.digitalWrite(OUT[2], LOW);
	elif menu ==6:
	    #ultrasonic
	    check_ultra();
	elif menu== 9:
		pca9685.go_right();
		time.sleep(20);
		pca9685.stop();
	elif menu== 10:
		pca9685.go_left();
		time.sleep(20);
		pca9685.stop();
	elif menu== 8:
		print("Beeping for 2 seconds\n");
		pca9685.on_buzz();
		time.sleep(20);
		pca9685.off_buzz();
		
	elif menu== 11:
		print("EXIT\n");
		keepRunning = 0;
			
	else:
		print("Check the list again\n")
			
	print("\n")
	menu = -1
def loop():
	"""//  return the cu
	time(el
	time since your arduino started) in milliseconds(1/1000 second)"""
	llinevalue = 0
	clinevalue = 0
	rlinevalue = 0
	
	print("This is a diagnostic program for your mobile robot.\n")
	print("0: go foward\n1: go backward\n2: front left led\n3: frount right led\n",
		"4: rear left led\n5: rear right led\n6: ultrasonic\n7: IR\n8: buzzer\n9:go right\n10: go left",
		"\n11: Exit the program\n")
	print("Please select one of them: ")
	menu = int(input())
	action(menu)
	menu = -1


"""// obstacle detection and move to another derection.
void checkUltra(){
	float disValue = ultra.ReadDista
	timeter();
    printf("ultrasonic: %f\n",disValue);
"""

def signal_handler(dummy):
	print("SIGNAL INTERRUPT",dummy)
	time.sleep(1000)
	keepRunning = 0;
#sda
    
def main (**kwargs):
    setup()
    signal.signal(signal.SIGINT, signal_handler)
    while keepRunning:
        loop()
    return 0

main()    
