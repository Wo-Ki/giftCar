# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/4/5 09:59

from . import *

from .baseCarCtrl import BaseCarCtrl


class CarCtrl(BaseCarCtrl):
    speed_l = 0.0
    speed_r = 0.0
    origin_wheel_value = 0

    def __init__(self, IN1, IN2, IN3, IN4, dir_pin):
        super(CarCtrl, self).__init__(IN1, IN2, IN3, IN4, dir_pin)

    # 定时测速
    def get_wheel_speed(self, value):
        pass

    # 从云端下发的原始数据
    def set_speed_value(self, value):
        self.origin_wheel_value = value
        self.left_wheel(value)
        self.right_wheel(value)
