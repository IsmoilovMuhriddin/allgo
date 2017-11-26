# Author: Muhriddin Ismoilov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from __future__ import division
import logging
import time
import math
import wiringpi as wp

# Registers/etc:
PCA9685_ADDRESS = 0x40
MODE1 = 0x00
MODE2 = 0x01
SUBADR1 = 0x02
SUBADR2 = 0x03
SUBADR3 = 0x04
PRESCALE = 0xFE
LED0_ON_L = 0x06
LED0_ON_H = 0x07
LED0_OFF_L = 0x08
LED0_OFF_H = 0x09
ALL_LED_ON_L = 0xFA
ALL_LED_ON_H = 0xFB
ALL_LED_OFF_L = 0xFC
ALL_LED_OFF_H = 0xFD

# Bits:
RESTART = 0x80
SLEEP = 0x10
ALLCALL = 0x01
INVRT = 0x10
OUTDRV = 0x04

LOW_PIN = 0
HIGH_PIN = 1

MAX_SPEED = 250
NOR_SPEED = 120
MIN_SPEED = 0

MOTOR_START_DELAY = 3

logger = logging.getLogger(__name__)


class PCA9685(object):
    """PCA9685 PWM LED/servo controller."""

    def __init__(self, address=PCA9685_ADDRESS, i2c=None, **kwargs):
        """Initialize the PCA9685."""
        # private variables of class
        # self.fd
        self.nSpeed = NOR_SPEED
        self.enAPin = 0
        self.en1Pin = 1
        self.en2Pin = 2
        self.enBPin = 5
        self.en3Pin = 3
        self.en4Pin = 4
        self.BuzzPin = 8
        self.fd = wp.wiringPiI2CSetup(0x60);
        self.init_start()

    def init_start(self):
        # Setup I2C interface for the device.

        self.set_all_pwm(0, 0)
        wp.wiringPiI2CWriteReg8(self.fd, MODE1, OUTDRV);
        wp.wiringPiI2CWriteReg8(self.fd, MODE1, ALLCALL);
        time.sleep(0.005)  # wait for oscillator
        mode1 = wp.wiringPiI2CReadReg8(self.fd, MODE1);
        mode1 = mode1 & ~SLEEP;  # wake up (reset sleep)
        wp.wiringPiI2CWriteReg8(self.fd, MODE1, mode1);
        time.sleep(0.005)  # wait for oscillator
        self.set_pwm_freq(1000)

    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0  # 25MHz
        prescaleval /= 4096.0  # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 0.5
        logger.debug('Setting PWM frequency to {0} Hz'.format(freq_hz))
        logger.debug('Estimated pre-scale: {0}'.format(prescaleval))
        prescale = int(math.floor(prescaleval + 0.5))
        logger.debug('Final pre-scale: {0}'.format(prescale))
        oldmode = wp.wiringPiI2CReadReg8(self.fd, MODE1);
        newmode = (oldmode & 0x7F) | 0x10;
        wp.wiringPiI2CWriteReg8(self.fd, MODE1, newmode)  # go to sleep
        wp.wiringPiI2CWriteReg8(self.fd, PRESCALE, prescale)
        wp.wiringPiI2CWriteReg8(self.fd, MODE1, oldmode)
        time.sleep(0.005)
        wp.wiringPiI2CWriteReg8(self.fd, MODE1, oldmode | 0x80)

    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        wp.wiringPiI2CWriteReg8(self.fd, LED0_ON_L + 4 * channel, on & 0xFF)
        wp.wiringPiI2CWriteReg8(self.fd, LED0_ON_H + 4 * channel, on >> 8)
        wp.wiringPiI2CWriteReg8(self.fd, LED0_OFF_L + 4 * channel, off & 0xFF)
        wp.wiringPiI2CWriteReg8(self.fd, LED0_OFF_H + 4 * channel, off >> 8)

    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        wp.wiringPiI2CWriteReg8(self.fd, ALL_LED_ON_L, on & 0xFF)
        wp.wiringPiI2CWriteReg8(self.fd, ALL_LED_ON_H, on >> 8)
        wp.wiringPiI2CWriteReg8(self.fd, ALL_LED_OFF_L, off & 0xFF)
        wp.wiringPiI2CWriteReg8(self.fd, ALL_LED_OFF_H, off >> 8)

    def set_pin(self, pin, value):
        if value == 0:
            self.set_pwm(pin, 0, 4096)
        if value == 1:
            self.set_pwm(pin, 4096, 0)

    def go_forward(self, speed_cur=-1):
        self.set_pin(self.en1Pin, HIGH_PIN)
        self.set_pin(self.en2Pin, LOW_PIN)

        self.set_pin(self.en3Pin, HIGH_PIN)
        self.set_pin(self.en4Pin, LOW_PIN)
        if speed_cur==-1:
            speed_cur=self.nSpeed
        self.set_speed(self.enAPin, speed_cur)
        self.set_speed(self.enBPin, speed_cur)

    def go_back(self, speed_cur=-1):
        self.set_pin(self.en1Pin, LOW_PIN)
        self.set_pin(self.en2Pin, HIGH_PIN)

        self.set_pin(self.en3Pin, LOW_PIN)
        self.set_pin(self.en4Pin, HIGH_PIN)
        if speed_cur==-1:
            speed_cur=self.nSpeed
        self.set_speed(self.enAPin, speed_cur)
        self.set_speed(self.enBPin, speed_cur)

    def go_left(self, speed_cur=-1,turning_rate=0.5):
        self.set_pin(self.en1Pin, LOW_PIN)
        self.set_pin(self.en2Pin, HIGH_PIN)

        self.set_pin(self.en3Pin, HIGH_PIN)
        self.set_pin(self.en4Pin, LOW_PIN)
        if speed_cur==-1:
            speed_cur=self.nSpeed

        self.set_speed(self.enAPin, int(speed_cur * turning_rate))
        self.set_speed(self.enBPin, speed_cur)

    def go_right(self, speed_cur=-1,turning_rate=0.5):
        self.set_pin(self.en1Pin, HIGH_PIN)
        self.set_pin(self.en2Pin, LOW_PIN)

        self.set_pin(self.en3Pin, LOW_PIN)
        self.set_pin(self.en4Pin, HIGH_PIN)
        if speed_cur==-1:
            speed_cur=self.nSpeed
        self.set_speed(self.enAPin, speed_cur)
        self.set_speed(self.enBPin, int(speed_cur * turning_rate))

    def stop(self):
        self.set_speed(self.enAPin, 0);
        self.set_speed(self.enBPin, 0);
    def stop_extreme(self):
        self.set_pin(self.en1Pin, LOW_PIN)
        self.set_pin(self.en2Pin, LOW_PIN)

        self.set_pin(self.en3Pin, LOW_PIN)
        self.set_pin(self.en4Pin, LOW_PIN)

    def set_speed(self, pin, speed):
        if (speed < 0):
            speed = 0
        if (speed > 255):
            speed = 255
        self.set_pwm(pin, 0, speed * 16)

    def set_normal_speed(self, speed):
        self.nSpeed = speed;

    def on_buzz(self):
        self.set_pwm(self.BuzzPin, 0, 2048)

    def off_buzz(self):
        self.set_pin(self.BuzzPin, 0)
