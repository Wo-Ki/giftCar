# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/31 15:35

from __future__ import division
import RPi.GPIO as gpio
import time
import Adafruit_PCA9685
import math


class Car_pwm_ctrl(object):
    """"""
    # 设置舵机活动范围
    servo_min = 200  # Min pulse length out of 4096
    servo_center = 300
    servo_max = 400  # Max pulse length out of 4096
    servo_angle = 0.03  # sleep时间，值越大，一次的转动幅度越大
    servo_Dvalue = 0.01  # 控制左右旋转产生的误差

    def __init__(self, IN1, IN2, IN3, IN4, dir_pin):
        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4
        self.dir_pin = dir_pin

        gpio.setmode(gpio.BOARD)

        gpio.setup(self.IN1, gpio.OUT)
        gpio.setup(self.IN2, gpio.OUT)
        gpio.setup(self.IN3, gpio.OUT)
        gpio.setup(self.IN4, gpio.OUT)

        hz = 400
        self.in1_hz = gpio.PWM(self.IN1, hz)
        self.in2_hz = gpio.PWM(self.IN2, hz)
        self.in3_hz = gpio.PWM(self.IN3, hz)
        self.in4_hz = gpio.PWM(self.IN4, hz)
        self.in1_hz.start(0)
        self.in2_hz.start(0)
        self.in3_hz.start(0)
        self.in4_hz.start(0)

        self.dir_pwm = Adafruit_PCA9685.PCA9685()
        self.dir_pwm.set_pwm_freq(60)
        # 初始归位方向轮
        self.dir_pwm.set_pwm(self.dir_pin, 0, self.servo_center)
        time.sleep(self.servo_angle - self.servo_Dvalue)
        self.dir_pwm.set_pwm(self.dir_pin, 0, 0)

    def left_wheel(self, value):
        """左轮的pwm控制"""
        # 前进
        if value > 0:
            self.in1_hz.changeDutyCycle(value)
            self.in2_hz.changeDutyCycle(0)
        # 后退
        elif value < 0:
            self.in1_hz.changeDutyCycle(100)
            self.in2_hz.changeDutyCycle(-value)
            # 停止
        else:
            self.in1_hz.changeDutyCycle(0)
            self.in2_hz.changeDutyCycle(0)

    def right_wheel(self, value):
        """右轮的pwm控制"""
        # 前进
        if value > 0:
            self.in3_hz.changeDutyCycle(value)
            self.in4_hz.changeDutyCycle(0)
        # 后退
        elif value < 0:
            self.in3_hz.changeDutyCycle(100)
            self.in4_hz.changeDutyCycle(-value)
            # 停止
        else:
            self.in3_hz.changeDutyCycle(0)
            self.in4_hz.changeDutyCycle(0)

    def dir_ctrl(self, value):
        """方向轮的pwm控制"""
        # 左转
        if value < 0:
            pwm_value = (-value / 100) * (self.servo_center - self.servo_min) + self.servo_min
            self.dir_pwm.set_pwm(self.dir_pin, 0, pwm_value)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.dir_pwm.set_pwm(self.dir_pin, 0, 0)
        # 右转
        elif value > 0:
            pwm_value = (value / 100) * (self.servo_max - self.servo_center) + self.servo_center
            self.dir_pwm.set_pwm(self.dir_pin, 0, pwm_value)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.dir_pwm.set_pwm(self.dir_pin, 0, 0)
        # 归位
        else:
            self.dir_pwm.set_pwm(self.dir_pin, 0, self.servo_center)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.dir_pwm.set_pwm(self.dir_pin, 0, 0)

    def stop(self):
        self.in1_hz.changeDutyCycle(0)
        self.in2_hz.changeDutyCycle(0)
        self.in3_hz.changeDutyCycle(0)
        self.in4_hz.changeDutyCycle(0)

    def all_die(self):
        self.in1_hz.stop()
        self.in2_hz.stop()
        self.in3_hz.stop()
        self.in4_hz.stop()
        gpio.cleanup()

if __name__ == "__main__":
    car_pwm_ctrl = Car_pwm_ctrl(29, 12, 15, 16, 0)
    car_pwm_ctrl.all_die()