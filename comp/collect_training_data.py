import SocketServer
import socket
import threading
import numpy as np
import cv2
import pygame
from pygame.locals import *
import socket
import time
import os
# SocketServer.ThreadingTCPServer.allow_reuse_address = True

RASP_IP = '192.168.43.70'
RASP_SERV_PORT = 7879
COMP_IP = '192.168.43.210'
COMP_SERV_PORT = 8002
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
"""
9x9 output
k = [
[1, 0, 0, 0, 0, 0, 0, 0, 0],    # left
[0, 1, 0, 0, 0, 0, 0, 0, 0],    # right
[0, 0, 1, 0, 0, 0, 0, 0, 0],    # forward
[0, 0, 0, 1, 0, 0, 0, 0, 0],    # reverse
[0, 0, 0, 0, 1, 0, 0, 0, 0],    # forward_left
[0, 0, 0, 0, 0, 1, 0, 0, 0],    # forward_right
[0, 0, 0, 0, 0, 0, 1, 0, 0],    # reverse_left
[0, 0, 0, 0, 0, 0, 0, 1, 0],    # reverse_right
[0, 0, 0, 0, 0, 0, 0, 0, 1],    # stop ~ reset

]


"""
class CollectTrainingData(object):
    def __init__(self):
        # creating server for camera
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((COMP_IP, COMP_SERV_PORT))
        self.server_socket.listen(0)

        # accept single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # create a socket and connect to motor controller
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((RASP_IP, RASP_SERV_PORT))

        self.send_motor = True

        self.k = np.zeros((4, 4), float)
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')

        pygame.init()

        self.collect_data()

    def collect_data(self):

        saved_frame = 0
        total_frame = 0

        # collect_images for training

        print 'Start collecting images'
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')

        # stream video frames one by one
        try:

            stream_bytes = ''
            frame = 1

            while self.send_motor:
                # print("reading data")
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                    # select lower half of the image
                    roi = image[120:240, :]

                    # save streamed images
                    cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)

                    # cv2.imshow('roi_image',roi)
                    cv2.imshow('image', image)

                    # reshape roi image in one array
                    temp_array = roi.reshape(1, 38400).astype(np.float32)

                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            # complex orders
                            if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                                print("Forward Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                # self.ser.write(chr(6))
                                self.client_socket.send(command['f_r'])

                            elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                                print("Forward Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                self.client_socket.send(command['f_l'])

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                                print("Reverse Right")
                                self.client_socket.send(command['rev_r'])

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                                print("Reverse Left")
                                self.client_socket.send(command['rev_l'])


                                # simple orders
                            elif key_input[pygame.K_UP]:
                                print("Forward")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                self.client_socket.send(command['f'])


                            elif key_input[pygame.K_DOWN]:
                                print("Reverse")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[3]))
                                self.client_socket.send(command['rev'])


                            elif key_input[pygame.K_RIGHT]:
                                print("Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                self.client_socket.send(command['r'])


                            elif key_input[pygame.K_LEFT]:
                                print("Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                self.client_socket.send(command['l'])


                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print 'exit'
                                self.send_motor = False
                                self.client_socket.send(command['rs'])
                                break

                        elif event.type == pygame.KEYUP:
                                self.client_socket.send(command['rs'])

                #print(stream_bytes)
                #self.client_socket.send(stream_bytes)

            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
            except IOError as e:
                print(e)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print 'Streaming duration:', time0

            print(train.shape)
            print(train_labels.shape)
            print 'Total frame:', total_frame
            print 'Saved frame:', saved_frame
            print 'Dropped frame', total_frame - saved_frame

        finally:
            self.connection.close()
            self.server_socket.close()
            self.client_socket.close()
if __name__ == '__main__':
    CollectTrainingData()
