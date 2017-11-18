import socket
RASP_IP = '192.168.137.174'
RASP_SERV_PORT = 7879


class MotorControl(object):
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((RASP_IP, RASP_SERV_PORT))
        self.server_socket.listen(0)

        self.connection = self.server_socket.accept()[0].makefile('rb')
        self.control()
    def control(self):
        received_command=0

        try:
            stream_bytes = ''
            while True:
                stream_bytes = self.connection.read()
                if not stream_bytes:
                    continue
                print(stream_bytes)


        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    MotorControl()
