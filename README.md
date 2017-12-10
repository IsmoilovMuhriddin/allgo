## allgo
 Capstone Project (Inha University, 2017 fall semester)
 Self Driving Car - System Self Driving car using color detection.
 ### Key Points
 * Two approach
    - Color Detection 
    - Neural Networks
    
 ##### Color Detection Approach 
 Two bootom frames checked for their colors and decision is made accordingly
 
 ![Cat](pic1.jpg)
 ```commandline
python rasp/autocar.py
```    

 ##### Neural Networks Approach
 Only Model creation stage is completed. Computer initialise server to collect camera data from raspberry takes input from keyboard where to go, and sends this data to raspberry to control motor. Simultaneously saves  frame and command in data array for model training.
 
 - Start MotorServer(motor_controller.py) from rasp
 - Start CompServer(collect_training_data.py) from comp
 - Start Camera Stream(camera_client.py) from rasp
 <br/><br/>_Now train data in your computer to get model_<br/>
 + run mlp_training.py in folder comp
 
 .........in progresss........<br/>
 ........wait for updates......
 
##### Requirements
Comp
- Opencv
- Tensorflow(optional for data)
```commandline
pip install wiringpi
pip install raspicam
```

##### 