
import time
import wiringpi

wiringpi.wiringPiSetupGpio()


LED_PIN =25


wiringpi.digitalWrite(LED_PIN,1)

while True:
    
    wiringpi.digitalWrite(LED_PIN,1)
    time.sleep(1)
    
    wiringpi.digitalWrite(LED_PIN,0)
    time.sleep(1)
