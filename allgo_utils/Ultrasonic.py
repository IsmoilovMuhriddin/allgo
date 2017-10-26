import wiringpi as wp
import time
LOW =0
HIGH =1
OUTPUT = wp.OUTPUT
INPUT = wp.INPUT

class ultrasonic(object):
    def __init__(self, trig,echo):
        self.trig = trig
        self.echo = echo
        self.end_time=0
        self.start_time=0
        wp.pinMode(self.trig,OUTPUT)
        wp.pinMode(self.echo,INPUT)
        wp.digitalWrite(self.trig,LOW)
        time.sleep(0.5)
    #here semms error on indent   
    def distance(self,timeout):
        wp.digitalWrite(self.trig,LOW)
        time.sleep(0.1)
    	wp.digitalWrite(self.trig,HIGH)
        # pulse 0.00001 = 10mikros
        time.sleep(0.00001)
        wp.digitalWrite(self.trig,LOW)
        
        now_time = time.time()
        while wp.digitalRead(self.echo)==LOW:
            #and time.time()-now_time<timeout):
            pulse_start = time.time()
        while wp.digitalRead(self.echo)==HIGH:
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
		
        
