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

    def __init__(self, IN1, IN2, IN3, IN4, dir_pin, yh_pin, yv_pin):
        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4
        self.dir_pin = dir_pin
        self.yh_pin = yh_pin
        self.yv_pin = yv_pin

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

        self.pca_pwm = Adafruit_PCA9685.PCA9685()
        self.pca_pwm.set_pwm_freq(60)
        # 初始归位方向轮
        self.pca_pwm.set_pwm(self.dir_pin, 0, self.servo_center)
        time.sleep(self.servo_angle - self.servo_Dvalue)
        self.pca_pwm.set_pwm(self.dir_pin, 0, 0)

    def left_wheel(self, value):
        """左轮的pwm控制"""
        # 后退
        if value > 0:
            self.in1_hz.ChangeDutyCycle(100 - value)
            self.in2_hz.ChangeDutyCycle(100)

        # 前进
        elif value < 0:
            self.in1_hz.ChangeDutyCycle(-value)
            self.in2_hz.ChangeDutyCycle(0)
        # 停止
        else:
            self.in1_hz.ChangeDutyCycle(0)
            time.sleep(0.01)
            self.in2_hz.ChangeDutyCycle(0)
            time.sleep(0.01)

    def right_wheel(self, value):
        """右轮的pwm控制"""
        # 后退
        if value > 0:
            self.in3_hz.ChangeDutyCycle(100 - value)
            self.in4_hz.ChangeDutyCycle(100)
        # 前进
        elif value < 0:

            self.in3_hz.ChangeDutyCycle(-value)
            self.in4_hz.ChangeDutyCycle(0)
            # 停止
        else:
            self.in3_hz.ChangeDutyCycle(0)
            self.in4_hz.ChangeDutyCycle(0)

    def dir_ctrl(self, value):
        """方向轮的pwm控制"""
        # 左转
        print "value:", value
        if value < 0:
            pwm_value = self.servo_center - ((-value) / 100.0) * (self.servo_center - self.servo_min)
            self.pca_pwm.set_pwm(self.dir_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.dir_pin, 0, 0)
        # 右转
        elif value > 0:
            pwm_value = (value / 100.0) * (self.servo_max - self.servo_center) + self.servo_center
            self.pca_pwm.set_pwm(self.dir_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.dir_pin, 0, 0)
        # 归位
        else:
            self.pca_pwm.set_pwm(self.dir_pin, 0, self.servo_center)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.dir_pin, 0, 0)

    def yh_ctrl(self, value):
        """云台水平方向控制"""
        yh_center = 375
        yh_max = 600
        yh_min = 150
        # 左转
        print "motion yh value:", value
        if value < 0:
            pwm_value = yh_center - ((-value) / 100.0) * (yh_center - yh_min)
            self.pca_pwm.set_pwm(self.yh_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.yh_pin, 0, 0)
        # 右转
        elif value > 0:
            pwm_value = (value / 100.0) * (yh_max - yh_center) + yh_center
            self.pca_pwm.set_pwm(self.yh_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.yh_pin, 0, 0)
        # 归位
        else:
            self.pca_pwm.set_pwm(self.yh_pin, 0, yh_center)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.yh_pin, 0, 0)

    def yv_ctrl(self, value):
        """云台垂直方向控制"""
        yv_center = 375
        yv_max = 600
        yv_min = 150
        # 左转
        print "motion yv value:", value
        if value < 0:
            pwm_value = yv_center - ((-value) / 100.0) * (yv_center - yv_min)
            self.pca_pwm.set_pwm(self.yv_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.yv_pin, 0, 0)
        # 右转
        elif value > 0:
            pwm_value = (value / 100.0) * (yv_max - yv_center) + yv_center
            self.pca_pwm.set_pwm(self.yv_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.yv_pin, 0, 0)
        # 归位
        else:
            self.pca_pwm.set_pwm(self.yv_pin, 0, yv_center)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.yv_pin, 0, 0)

    def stop(self):
        self.in1_hz.ChangeDutyCycle(0)
        self.in2_hz.ChangeDutyCycle(0)
        self.in3_hz.ChangeDutyCycle(0)
        self.in4_hz.ChangeDutyCycle(0)

    def all_die(self):
        self.in1_hz.stop()
        self.in2_hz.stop()
        self.in3_hz.stop()
        self.in4_hz.stop()
        gpio.cleanup()


if __name__ == "__main__":
    car_pwm_ctrl = Car_pwm_ctrl(13, 12, 15, 16, 0, 1, 2)
    # car_pwm_ctrl.left_wheel(50)
    # time.sleep(4)
    # car_pwm_ctrl.left_wheel(100)
    # time.sleep(4)
    # car_pwm_ctrl.left_wheel(0)
    car_pwm_ctrl.dir_ctrl(50)
    time.sleep(3)
    car_pwm_ctrl.dir_ctrl(0)
    time.sleep(3)
    car_pwm_ctrl.dir_ctrl(-50)
    time.sleep(3)
    car_pwm_ctrl.dir_ctrl(0)
    # car_pwm_ctrl.all_die()
