import wiringpi as wp
import time
LOW = 0
HIGH =1
OUTPUT = wp.OUTPUT
INPUT = wp.INPUT


MAX_SENSOR_DISTANCE	=	500
NO_ECHO	            =	0

class ultrasonic(object):
    def __init__(self, trig=3,echo=23):
        self.trig = trig
        self.echo = echo
        wp.pinMode(self.trig,OUTPUT)
        wp.pinMode(self.echo,INPUT)
        time.sleep(0.5)

    def distance(self):
        # pulse 0.00001 = 10mikros

        wp.digitalWrite(self.trig,LOW)
        time.sleep(0.1)
    	wp.digitalWrite(self.trig,HIGH)
        time.sleep(0.00001)
        wp.digitalWrite(self.trig,LOW)
        
        now_time = time.time()
        pulse_start=0
        pulse_end=0
        while wp.digitalRead(self.echo)== LOW:
            #and time.time()-now_time<timeout):
            pulse_start = time.time()
        while wp.digitalRead(self.echo)== HIGH:
            pulse_end=time.time()
        pulse_dur = pulse_end-pulse_start
        distance=round(pulse_dur*17000.0,2)

        #self.record_pulse_length()
        #time.sleep(1)
        #travel_time = self.end_time-self.start_time;
        #distanceMeters = 100*(travel_time*340.29)/2
        return distance
    def record_pulse_length(self):
        self.start_time=time.time()
        while ( wp.digitalRead(self.echo) == HIGH):
            pass
        self.end_time=time.time()
