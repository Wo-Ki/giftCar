# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/5/4 14:45

# from . import *

from __future__ import division
import RPi.GPIO as gpio
import time
import Adafruit_PCA9685
import math
import threading
import json
import threading


# echo = 33
# trig = 35


class RadarCtrl(object):
    """舵机＋sr04超声波雷达"""
    # 设置舵机活动范围
    servo_min = 180  # Min pulse length out of 4096
    servo_center = 320
    servo_max = 460  # Max pulse length out of 4096
    servo_angle = 0.03  # sleep时间，值越大，一次的转动幅度越大
    servo_Dvalue = 0.01  # 控制左右旋转产生的误差

    current_sr04_angle = servo_min  # 舵机起始位置
    current_sr04_distance = -1.0
    servo_dir = True  # 默认方向为True，逆向为False

    def __init__(self, servo_pin, echo_pin, trig_pin):
        """servo_pin为PCA9685上舵机的位置"""
        self.servo_pin = servo_pin
        self.echo_pin = echo_pin
        self.trig_pin = trig_pin

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(55)

        gpio.setmode(gpio.BOARD)
        gpio.setup(self.trig_pin, gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.echo_pin, gpio.IN)
        time.sleep(2)

    def get_servo_and_distance(self):
        self.pwm.set_pwm(self.servo_pin, 0, self.current_sr04_angle)
        time.sleep(self.servo_angle - self.servo_Dvalue)
        self.current_sr04_distance = self.get_distance()
        if self.servo_dir is True:
            self.current_sr04_angle += 2
        else:
            self.current_sr04_angle -= 2
        if self.current_sr04_angle > self.servo_max:
            self.servo_dir = False
        elif self.current_sr04_angle < self.servo_min:
            self.servo_dir = True

    def clear_servo(self):
        self.pwm.set_pwm(self.servo_pin, 0, 0)

    def get_distance(self):
        """通过sr04获取距离"""
        # 发出触发信号
        gpio.output(self.trig_pin, gpio.HIGH)
        # 保持10us以上（我选择15us）
        time.sleep(0.000015)
        gpio.output(self.trig_pin, gpio.LOW)

        while not gpio.input(self.echo_pin):
            pass
        # 发现高电平时开时计时
        t1 = time.time()
        while gpio.input(self.echo_pin):
            if time.time() - t1 >= 0.0588235:  # 超过10米终止,来回共20米的时间
                return  -1
        # 高电平结束停止计时
        t2 = time.time()
        # 返回距离，单位为米
        return (t2 - t1) * 340 / 2


if __name__ == "__main__":
    radarCtrl = RadarCtrl(7, 33, 35)
    try:
        while 1:
            pass
    except:
        radarCtrl.clear_servo()
    # gpio.cleanup()
    radarCtrl.clear_servo()
