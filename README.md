## allgo
 Capstone Project (Inha University, 2017 fall semester)
 Self Driving Car - System Self Driving car using color detection.
 ### Key Points
 * Two approach
    - Color Detection 
    - Neural Networks
    
 ##### Color Detection Approach 
 Two bottom frames checked for their colors and decision is made accordingly
 
 ![Cat](pics/pic1.jpg)
 ```commandline
python rasp/autocar.py
```    
<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vRCX5FwVTLh-jBEkWzX7Yslm6VVHjOoNLJOurFSI8OQ09s3ung_BhXZGYkRVYEF68yMnu_EkMQ0sMIn/embed?start=false&loop=false&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
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

<p>Sample</p>
<iframe width="560" height="315" src="https://www.youtube.com/embed/dHHmUF9gs70" frameborder="0" allowfullscreen></iframe>
<p>Presentation</p>
<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vRCX5FwVTLh-jBEkWzX7Yslm6VVHjOoNLJOurFSI8OQ09s3ung_BhXZGYkRVYEF68yMnu_EkMQ0sMIn/embed?start=true&loop=true&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>