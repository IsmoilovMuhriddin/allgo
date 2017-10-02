"""// diagnosis.cpp
#include <wiringPi.h>
#include <stdio.h>
#include "PCA9685.h"
#include "Ultrasonic.h"
#include <signal.h>"""

import Ardafruit_PCA as pca
import wiringpi as wp
import signal
import sys

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
 
pca9685 =pca.PCA9685()  # An instance of the motor & buzzer
#Ultrasonic ultra; # An instance of the ultrasonic sensor
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
	wp.wp.digitalWrite(OUT[i], LOW_PIN)
    for i in range(len(IN)):
        wp.pinMode(IN[i],INPUT)
def action(menu):
   	global curMillis

	if menu==0:
		pca9685.go_forward();
		delay(500);
		pca9685.stop();
		
	elif menu== 1:
		pca9685.go_back();
		delay(500);
		pca9685.stop();
		
	elif menu== 2:
		# frount left
		wp.digitalWrite(OUT[0], HIGH);
		delay(50);
		wp.digitalWrite(OUT[0], LOW);
		delay(50);
		wp.digitalWrite(OUT[0], HIGH);
		delay(50);
		wp.digitalWrite(OUT[0], LOW);
		
	elif menu== 3:
		#// frount right
		wp.digitalWrite(OUT[1], HIGH);
		delay(50);
		wp.digitalWrite(OUT[1], LOW);
		delay(50);
		wp.digitalWrite(OUT[1], HIGH);
		delay(50);
		wp.digitalWrite(OUT[1], LOW);
		
	elif menu== 4:
		#// rear left
		wp.digitalWrite(OUT[3], HIGH);
		delay(50);
		wp.digitalWrite(OUT[3], LOW);
		delay(50);
		wp.digitalWrite(OUT[3], HIGH);
		delay(50);
		wp.digitalWrite(OUT[3], LOW);
		
	elif menu== 5:
		# rear right
		wp.digitalWrite(OUT[2], HIGH);
		delay(50);
		wp.digitalWrite(OUT[2], LOW);
		delay(50);
		wp.digitalWrite(OUT[2], HIGH);
		delay(50);
		wp.digitalWrite(OUT[2], LOW);
		
	elif menu== 8:
		printf("Beeping for 2 seconds\n");
		pca9685.on_buzz();
		delay(2000);
		pca9685.off_buzz();
		break;
	elif menu== 11:
		printf("EXIT\n");
		keepRunning = 0;
			
	else:
		print("Check the list again\n")
			
	print("\n")
	menu = -1
def loop():
	"""//  return the current time(elapsed time since your arduino started) in milliseconds(1/1000 second)"""
	llinevalue = 0
	clinevalue = 0
	rlinevalue = 0
	action(menu)
	menu = -1
	print("This is a diagnostic program for your mobile robot.\n")
	print("0: go foward\n1: go backward\n2: front left led\n3: frount right led\n4: rear left led\n5: rear right led\n6: ultrasonic\n7: IR\n8: buzzer\n11: Exit the program\n")
	print("Please select one of them: ")
	menu = int(input())
	
	


"""// obstacle detection and move to another derection.
void checkUltra(){
	float disValue = ultra.ReadDistanceCentimeter();
    printf("ultrasonic: %f\n",disValue);
"""

def signal_handler(dummy):
        print("SIGNAL INTERRUPT",dummy)
        time.sleep(1000)      
        keepRunning = 0;
signal.signal(signal.SIGINT, signal_handler)

    
def main (**kwargs):
    setup()
    signal(SIGINT, intHandler)
    while keepRunning:
    	loop()
    return 0

main()    
