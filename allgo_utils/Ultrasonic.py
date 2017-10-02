import wirinpi as wp
import time
LOW =0
HIGH =1
OUTPUT = wp.OUTPUT
INPUT = wp.INPUT

class Ultrasonic(object):
	def __init__(self, trig,echo):
		self.trig = trig
		self.echo = echo
		self.end_time=0
		self.start_time=0
		wp.pinMode(self.trig,OUTPUT)
		wp.pinMode(self.echo,INPUT)
		wp.digitalWrite(self.trig,LOW)
		time.sleep(0.5)
       
    def distance(self,timeout):
<<<<<<< HEAD
        time.sleep(0.01):
            wp.digitalWrite(self.trig,HIGH)
            time.sleep(0.01)
    	wp.digitalWrite(self.trig,LOW)
=======
        time.sleep(0.01)
        wp.digitalWrite(self.trig,HIGH)
        time.sleep(0.01)
        wp.digitalWrite(self.trig,LOW)
>>>>>>> 8396b8269e42b739ca9c9806d36108a4b4e4ee75

        now_time = time.time()
        while wp.digitalRead(self.echo==LOW and time.time()-now_time<timeout):
            pass
        self.record_pulse_length()
        travel_time = self.end_time-self.start_time;
        distanceMeters = 100*(travel_time*340.29)/2
        return distanceMeters
    def record_pulse_length(self):
        self.start_time=time.time()
        while ( wp.digitalRead(self.echo) == HIGH):
            pass
        self.start_time=time.time()         

        
