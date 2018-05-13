# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/3/25 19:16

from . import *


class ServoCtrl(object):
    """舵机控制类"""
    # 设置舵机活动范围
    servo_min = 200  # Min pulse length out of 4096
    servo_center = 300
    servo_max = 400  # Max pulse length out of 4096
    servo_angle = 0.03  # sleep时间，值越大，一次的转动幅度越大
    servo_Dvalue = 0.01  # 控制左右旋转产生的误差

    def __init__(self, yh_pin, yv_pin):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(55)
        self.yh_pin = yh_pin
        self.yv_pin = yv_pin

    def yh_ctrl(self, value, lock=True):
        """云台水平方向控制"""
        yh_center = 375
        yh_max = 600
        yh_min = 150
        # 左转
        print("motion yh value:", value)
        if value < 0:
            pwm_value = (-value / 100.0) * (yh_max - yh_center) + yh_center
            self.pwm.set_pwm(self.yh_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            if lock is False:
                self.pwm.set_pwm(self.yh_pin, 0, 0)
        # 右转
        elif value > 0:
            pwm_value = yh_center - (value / 100.0) * (yh_center - yh_min)
            self.pwm.set_pwm(self.yh_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            if lock is False:
                self.pwm.set_pwm(self.yh_pin, 0, 0)

        # 归位
        else:
            self.pwm.set_pwm(self.yh_pin, 0, yh_center)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            if lock is False:
                self.pwm.set_pwm(self.yh_pin, 0, 0)

    def yv_ctrl(self, value, lock=True):
        """云台垂直方向控制"""
        yv_center = 375
        yv_max = 600
        yv_min = 150
        # 左转
        print("motion yv value:", value)
        if value < 0:
            pwm_value = yv_center - ((-value) / 100.0) * (yv_center - yv_min)
            self.pwm.set_pwm(self.yv_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            if lock is False:
                self.pwm.set_pwm(self.yv_pin, 0, 0)
        # 右转
        elif value > 0:
            pwm_value = (value / 100.0) * (yv_max - yv_center) + yv_center
            self.pwm.set_pwm(self.yv_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            if lock is False:
                self.pwm.set_pwm(self.yv_pin, 0, 0)
        # 归位
        else:
            self.pwm.set_pwm(self.yv_pin, 0, yv_center)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            if lock is False:
                self.pwm.set_pwm(self.yv_pin, 0, 0)
