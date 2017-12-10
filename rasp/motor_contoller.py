import socket
from  allgo_utils import PCA9685,ultrasonic,ir_sens


RASP_IP = '192.168.43.70'
RASP_SERV_PORT = 7879

command = {
    # single commands
    'rs': "rst_:",
    'f': "fwd_:",
    'rev': "rev_:",
    'r': "rht_:",
    'l': "lft_:",
    # combination commands
    'f_r': "f_rt:",
    'f_l': "f_lf:",
    'rev_r': "rv_r:",
    'rev_l': "rv_l:",
# 5 character in each string
}

class MotorControl(object):
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((RASP_IP, RASP_SERV_PORT))
        self.server_socket.listen(0)
        self.pca = PCA9685()
        self.connection = self.server_socket.accept()[0].makefile('rb')
        self.control()
    def control(self):
        received_command=0

        try:
            stream_bytes = ''
            while True:
                stream_bytes = self.connection.read(5)
                if not stream_bytes:
                    continue
                if stream_bytes == command['f']:
                    self.pca.go_forward()
                elif stream_bytes == command['f_l']:
                    self.pca.go_left()
                elif stream_bytes == command['f_r']:
                    self.pca.go_right()
                elif stream_bytes == command['r']:
                    self.pca.go_right(turning_rate=0)
                elif stream_bytes == command['l']:
                    self.pca.go_left(turning_rate=0)
                elif stream_bytes == command['rev']:
                    self.pca.go_back()
                elif stream_bytes == command['rev_l']:
                    self.pca.go_rev_left()
                elif stream_bytes == command['rev_r']:
                    self.pca.go_rev_right()
                elif stream_bytes == command['rs']:
                    self.pca.stop()
                else:
                    self.pca.stop()




        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    MotorControl()
