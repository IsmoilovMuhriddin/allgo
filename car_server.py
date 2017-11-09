import threading
import SocketServer
import serial
import cv2
import numpy as np
import math
# distance data measured by ultrasonic sensor
sensor_data = " "

class DistanceToCamera(object):

    def __init__(self):
        # camera params
        self.alpha = 8.0 * math.pi / 180
        self.v0 = 119.865631204
        self.ay = 332.262498472

    def calculate(self, v, h, x_shift, image):
        # compute and return the distance from the target point to the camera
        d = h / math.tan(self.alpha + math.atan((v - self.v0) / self.ay))
        if d > 0:
            cv2.putText(image, "%.1fcm" % d,
                (image.shape[1] - x_shift, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return d


class SensorDataHandler(SocketServer.BaseRequestHandler):

    data = " "

    def handle(self):
        global sensor_data
        try:
            while self.data:
                self.data = self.request.recv(1024)
                #3sensor_data = round(float(self.data), 1)
                #print "{} sent:".format(self.client_address[0])
                #sensor_data
                print self.data
        finally:
            print "Connection closed on thread 2"



class VideoStreamHandler(SocketServer.StreamRequestHandler):

    # h1: stop sign
    h1 = 15.5 - 10  # cm
    # h2: traffic light
    h2 = 15.5 - 10
    d_to_camera = DistanceToCamera()

    def handle(self):
        global sensor_data
        stream_bytes = ' '
        stop_flag = False
        stop_sign_active = True
        # stream video frames one by one
        try:
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last+2]
                    stream_bytes = stream_bytes[last+2:]
                    #gray = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    #image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)

                    # lower half of the image
                    half_gray = gray[120:240, :]


                    cv2.imshow('image', jpg)
                # cv2.imshow('mlp_image', half_gray)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.rc_car.stop()
                    break
            cv2.destroyAllWindows()
        finally:
            print "Connection closed on thread 1"
class ThreadServer(object):

    def server_thread(host, port):
        server = SocketServer.TCPServer((host, port), VideoStreamHandler)
        server.serve_forever()

    def server_thread2(host, port):
        server = SocketServer.TCPServer((host, port), SensorDataHandler)
        server.serve_forever()

    distance_thread = threading.Thread(target=server_thread2, args=('localhost', 8004))
    distance_thread.start()

    video_thread = threading.Thread(target=server_thread('localhost', 8002))
    video_thread.start()
if __name__ == '__main__':
    ThreadServer()