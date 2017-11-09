from socket import *
import time
from allgo_utils import *
ULTRASONIC_TRIG	= 3 # TRIG port is to use as output signal
ULTRASONIC_ECHO = 23 # ECHO port is to use as input signal



client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect(('localhost',8004))
ult=ultrasonic(ULTRASONIC_TRIG,ULTRASONIC_ECHO)


try:
    while True:
        dist= ult.distance()
        print "Distance: %.1f cm" % dist
        client_socket.send(str(dist))
        time.sleep(0.1)
finally:
    client_socket.close()




