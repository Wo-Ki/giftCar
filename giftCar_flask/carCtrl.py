# coding:utf-8

import RPi.GPIO as gpio
import time
from __future__ import division
import Adafruit_PCA9685
import math


class CarCtrlClass(object):
    # 设置舵机活动范围
    servo_min = 200  # Min pulse length out of 4096
    servo_center = 300
    servo_max = 400  # Max pulse length out of 4096
    servo_angle = 0.03  # sleep时间，值越大，一次的转动幅度越大
    servo_Dvalue = 0.01  # 控制左右旋转产生的误差

    def __init__(self, IN1, IN2, IN3, IN4, servoPin):
        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4
        self.servoPin = servoPin

        gpio.setmode(gpio.BOARD)
        gpio.setup(self.IN1, gpio.OUT)
        gpio.setup(self.IN2, gpio.OUT)
        gpio.setup(self.IN3, gpio.OUT)
        gpio.setup(self.IN4, gpio.OUT)

        self.stop()

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)

    def go(self, value):
        if value == True:
            gpio.output(self.IN1, 1)
            gpio.output(self.IN2, 0)
            gpio.output(self.IN3, 1)
            gpio.output(self.IN4, 0)
        else:
            self.stop()

    def down(self, value):
        if value == True:
            gpio.output(self.IN1, 0)
            gpio.output(self.IN2, 1)
            gpio.output(self.IN3, 0)
            gpio.output(self.IN4, 1)
        else:
            self.stop()

    def left(self, value):
        if value == True:
            self.pwm(self.servoPin, 0, self.servo_min)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pwm(self.servoPin, 0, 0)
        else:
            self.pwm(self.servoPin, 0, self.servo_center)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pwm(self.servoPin, 0, 0)

    def right(self, value):
        if value == True:
            self.pwm(self.servoPin, 0, self.servo_max)
            time.sleep(self.servo_angle)
            self.pwm(self.servoPin, 0, 0)
        else:
            self.pwm(self.servoPin, 0, self.servo_center)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pwm(self.servoPin, 0, 0)

    def stop(self):
        gpio.output(self.IN1, 0)
        gpio.output(self.IN2, 0)
        gpio.output(self.IN3, 0)
        gpio.output(self.IN4, 0)

    def set_servo_pulse(self, channel, pulse):
        pulse_length = 1000000  # 1,000,000 us per second
        pulse_length //= 60  # 60 Hz
        print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096  # 12 bits of resolution
        print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        self.pwm.set_pwm(channel, 0, pulse)


if __name__ == "__main__":
    myCar = CarCtrlClass(29, 12, 15, 16, 0)
    myCar.stop()
