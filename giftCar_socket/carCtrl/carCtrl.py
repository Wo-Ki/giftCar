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

    avoid_up_left = False
    avoid_up_right = False
    avoid_down_left = False
    avoid_down_right = False

    def __init__(self, IN1, IN2, IN3, IN4, dir_pin, avoid_up_left_pin, avoid_down_left_pin):
        super(CarCtrl, self).__init__(IN1, IN2, IN3, IN4, dir_pin)
        self.avoid_up_left_pin = avoid_up_left_pin
        self.avoid_down_left_pin = avoid_down_left_pin
        gpio.setup(avoid_up_left_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(avoid_down_left_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(avoid_up_left_pin, gpio.BOTH, callback=self.avoid_up_left_changed)
        gpio.add_event_detect(avoid_down_left_pin, gpio.BOTH, callback=self.avoid_down_left_changed)

    # 定时测速
    def get_wheel_speed(self, value):
        pass

    # 从云端下发的原始数据
    def set_speed(self, value):
        self.origin_wheel_value = value
        if (value > 0 and self.avoid_down_left is False) or (value < 0 and self.avoid_up_left is False) or value == 0:
            self.left_wheel(value)
            self.right_wheel(value)

    def avoid_up_left_changed(self, channel):
        if gpio.event_detected(self.avoid_up_left_pin):
            if gpio.input(self.avoid_up_left_pin) == gpio.LOW:
                self.avoid_up_left = True
                if self.origin_wheel_value < 0:
                    self.set_speed(0)
                print "self.avoid_up_left:", self.avoid_up_left
            else:
                self.avoid_up_left = False
                print "self.avoid_up_left:", self.avoid_up_left

    def avoid_down_left_changed(self, channel):
        if gpio.event_detected(self.avoid_down_left_pin):
            if gpio.input(self.avoid_down_left_pin) == gpio.LOW:
                self.avoid_down_left = True
                if self.origin_wheel_value > 0:
                    self.set_speed(0)
                print "self.avoid_down_left:", self.avoid_down_left
            else:
                self.avoid_down_left = False
                print "self.avoid_down_left:", self.avoid_down_left
