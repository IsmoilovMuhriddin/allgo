from socket import *
import time
from allgo_utils import *



client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect(('127.0.0.1',8004))
ult=ultrasonic()


try:
    while True:
        distance = ult.distance()
        print "Distance: %.1f cm" % distance
        client_socket.send(str(distance))
finally:
    client_socket.close()



