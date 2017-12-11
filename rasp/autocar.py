# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from  allgo_utils import PCA9685,ultrasonic,ir_sens
import wiringpi as wp

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(320,240))
bound = [([17,15,100],[50,56,200])]
# capture frames from the camera


DIR_DISTANCE_ALERT = 20
preMillis = 0

ULTRASONIC_TRIG	= 3 # TRIG port is to use as output signal
ULTRASONIC_ECHO = 23 # ECHO port is to use as input signal
OUT = {'front_left_led':5,
       'front_right_led':0,
       'rear_right_led':1,
       'rear_left_led':2,
       'ultra_trig':3} # 5:front_left_led, 0:front_right_led, 1:rear_right_led, 2:rear_left_led, 3:ultra_trig
IN = {'left_IR':21,
      'center_IR':22,
      'right_IR':26,
      'ultra_echo':23} # 21:left_IR, 22:center_IR, 26:right_IR, 23:ultra_echo


LOW = 0
HIGH = 1
OUTPUT = wp.OUTPUT
INPUT = wp.INPUT


pca = PCA9685()
uls = ultrasonic(ULTRASONIC_TRIG,ULTRASONIC_ECHO)
def setup():
    wp.wiringPiSetup()  # Initialize wiringPi to load Raspbarry Pi PIN numbering scheme
    for key in OUT:
        wp.pinMode(OUT[key],OUTPUT)
        wp.digitalWrite(OUT[key], LOW)
    for key in IN:
        wp.pinMode(IN[key],INPUT)
        
def warn(times=3):
    for i in range(times):
        wp.digitalWrite(OUT['front_right_led'], HIGH)
        wp.digitalWrite(OUT['front_left_led'], HIGH)

        wp.digitalWrite(OUT['rear_right_led'], HIGH)
        wp.digitalWrite(OUT['rear_left_led'], HIGH)
        time.sleep(0.15)

        wp.digitalWrite(OUT['front_right_led'], LOW)
        wp.digitalWrite(OUT['front_left_led'], LOW)

        wp.digitalWrite(OUT['rear_right_led'], LOW)
        wp.digitalWrite(OUT['rear_left_led'], LOW)
        time.sleep(0.15)        

# WHITE SECTION
def detectPedestrian(img):
    detected = 'no'
    crop_img = img[40:100, 100:220]
    lower_white = np.array([0, 0, 0])
    upper_white = np.array([0, 0, 255])
    hsv = cv2.cvtColor(crop_img,cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    number_of_white_px = np.count_nonzero(white_mask)
    if (number_of_white_px>300):
        detected = 'pedes'
    print (number_of_white_px)
    res = cv2.bitwise_and(crop_img, crop_img, mask=white_mask)
    #cv2.imshow("detected", crop_img)
    #cv2.imshow('result_mask', white_mask)
    #cv2.imshow('result_color', res)

    return detected
# detect RED
def detectRed(img,count=7,bottom=False,first=False):
    detected = 'no'
    if bottom==True:
        crop_img=img[180:,:]
    elif first==True:
        crop_img = img[40:100,160:240]
    else:
        crop_img = img[40:100,240:320]

    lower_red_1 = np.array([170, 100, 100])
    upper_red_1 = np.array([180, 255, 255])

    lower_red_2 = np.array([0, 100, 100])
    upper_red_2 = np.array([10, 255, 255])


    hsv = cv2.cvtColor(crop_img,cv2.COLOR_BGR2HSV)

    red_mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    red_mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    red_mask = red_mask_1 + red_mask_2

    number_of_white_px = np.count_nonzero(red_mask)
    if (number_of_white_px>count):
        detected = 'red'
    print("RED numbers:",number_of_white_px)
    res = cv2.bitwise_and(crop_img, crop_img, mask=red_mask)
    #cv2.imshow("detected", crop_img)
    #cv2.imshow('result_mask', red_mask)
    #cv2.imshow('result_color', res)

    return detected

def yellow_pixel_count(img,side):

    lower_black = np.array([0,0,0])
    upper_black = np.array([120, 100, 100])

    lower_yellow = np.array([20, 120, 80])
    upper_yellow = np.array([40, 200, 255])


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    black_mask = cv2.inRange(hsv,lower_black, upper_black)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_masked_color = cv2.bitwise_and(img, img, mask=yellow_mask)
    number_of_yellow_pixel = np.count_nonzero(yellow_mask)
    #number_of_yellow_pixel = np.count_nonzero(black_mask)
    #cv2.imshow("right",black_mask)
    print(number_of_yellow_pixel,side)
    
    return [number_of_yellow_pixel,img]
#DEFAULT IMAGE ANALYSIS
def show(img):
    # TO DO receive imgs from raspicam
    
    img_left = img[210:240, 5:115]
    img_right = img[210:240, 205:315]

    margin = 250

    yellow_pxs_left,img_left = yellow_pixel_count(img_left,' left')
    yellow_pxs_right,img_right= yellow_pixel_count(img_right,' right')
    #cv2.imread("allgo",img)
    #cv2.imread("right",img_right)
    #cv2.imread("left",img_left)
    
    
    if (yellow_pxs_left>margin and yellow_pxs_right>margin):
        print ("go forward")
        return 'f'
    elif (yellow_pxs_left>margin and yellow_pxs_right<margin):
        """"if yellow_pxs_right==0:
            print("go forward_right")
            return 'f_r'"""
        print ("go right")
        return 'r'
    elif (yellow_pxs_left<margin and yellow_pxs_right>margin):
        """if yellow_pxs_left==0:
            print("go forward_left")
            return 'f_l'"""
        print ("go left")
        return 'l'
    elif((yellow_pxs_right<margin and yellow_pxs_left<margin) and
         yellow_pxs_left<yellow_pxs_right):
        if yellow_pxs_left==0:
            print("go forward_left sps")
            return 'l'
        
        print ("go left sps case")
        return 'l' 
    elif ((yellow_pxs_right < margin and yellow_pxs_left < margin) and
                  yellow_pxs_left > yellow_pxs_right):
        if yellow_pxs_left==0:
            print("go forward_right sps")
            return 'r'
        
        print ("go right sps case")
        return 'r'
    elif (yellow_pxs_right==0 and yellow_pxs_left ==0):
        print ("go forward zeros")
        return 'f_z'
    else:
        print('left '+str(yellow_pxs_left)+'\nright '+str(yellow_pxs_right))
        return 's'

def way(move):
    if move == 'f':
        pca.go_forward(speed_cur=80, delay=0.02)
    elif move == 'f_z':
        pca.go_forward(speed_cur=80, delay=0.02)
    elif move == 'l':
        pca.go_left(speed_max=75, speed_norm=0, delay=0.02, motor_back=True)
    # pca.go_forward(delay=0.01)
    elif move == 'r':
        pca.go_right(speed_max=75, speed_norm=0, delay=0.02, motor_back=True)
    # pca.go_forward(delay=0.01)
    elif move == 'f_l':
        pca.go_left(speed_max=140, speed_norm=70, delay=0.02, motor_back=False)
    elif move == 'f_r':
        pca.go_right(speed_max=140, speed_norm=70, delay=0.02, motor_back=False)
    elif move=='sleep':
        time.sleep(0.02)
    else:
        pca.stop()
def parking(f_time=1.1,left=True):
    pca.go_forward(delay=f_time)
    pca.go_left(speed_max=120, speed_norm=70, delay=0.7, motor_back=True)
    pca.go_back(delay=0.5)
    pca.stop()
def main():
    pca.set_normal_speed(80)
    first_turn = True
    first_obstacle=True
    first_obstacle_found=False
    pedestrian=True
    move_prev='ba'
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img=frame.array
        move=show(img)
        changed=move is move_prev
        move_prev=move
        #x=detectRed(img,count=7)
        if changed==True:
            move=move
        distance=uls.distance()
        cv2.imshow("allgo", img)
        if first_turn:
            #print(detectRed(img=img))
            if (detectRed(img,count=7,first=True)=='red'):
                move='stop'
                move_prev=move
                #pca.stop()
                way(move)
            else:
                pca.go_forward(speed_cur=120,delay=1.1)
                
                pca.go_right(delay=0.6, speed_max=120, speed_norm=85,motor_back=True)
                pca.go_forward(speed_cur=100,delay=0.5)
                first_turn = False

        elif first_obstacle:
            if distance < 20:
                print("Obstacle identified, distance=", distance)
                pca.go_right(speed_max=100, speed_norm=60, delay=0.5, motor_back=True)
                first_obstacle_found=True
            else:
                way(move)
            if first_obstacle_found:
                first_obstacle=False
        else:
            
            if(detectRed(img,count=2000,bottom=True)=='red'):
                move='stop'
                move_prev=move
                way(move)
                time.sleep(0.5)
                parking()
                
                print("............PARKING DETECTED...........")
                break
            elif(detectRed(img,count=200)=='red'):
                move='stop'
                move_prev=move
                way(move)
                print("<<<<<<<<<RED STOP>>>>>>>>") 
            elif distance<30:
                move='stop'
                move_prev=move
                if detectPedestrian(img)=='pedes':
                    print("pedestrian")
                    #pca.stop()
                    way(move)
                else:
                    way(move)
                    #pca.stop()
                    print("Distance!!!! = ",distance)
                    warn()
            else:
                way(move)
        rawCapture.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        
        if key == ord("q"):
            break
setup()        
while True:
    main()