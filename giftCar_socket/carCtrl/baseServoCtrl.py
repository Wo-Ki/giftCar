# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/3/25 19:16

from . import *


class baseServoCtrl(object):
    """舵机控制类"""
    # 设置舵机活动范围
    servo_min = 200  # Min pulse length out of 4096
    servo_center = 300
    servo_max = 400  # Max pulse length out of 4096
    servo_angle = 0.03  # sleep时间，值越大，一次的转动幅度越大
    servo_Dvalue = 0.01  # 控制左右旋转产生的误差

    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(65)

    def set(self, pin, value, lock=False):
        pass
