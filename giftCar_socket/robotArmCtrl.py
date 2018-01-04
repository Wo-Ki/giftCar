# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/1/4 08:11 

from __future__ import division
import RPi.GPIO as gpio
import time
import Adafruit_PCA9685
import math


class RobotArmCtrl(object):
    """机械臂控制类"""
    # 设置舵机活动范围
    servo_min = 200  # Min pulse length out of 4096
    servo_center = 300
    servo_max = 400  # Max pulse length out of 4096
    servo_angle = 0.03  # sleep时间，值越大，一次的转动幅度越大
    servo_Dvalue = 0.01  # 控制左右旋转产生的误差

    def __init__(self, downPin, leftPin, rightPin, upPin):
        self.pca_pwm = Adafruit_PCA9685.PCA9685()
        self.pca_pwm.set_pwm_freq(60)
        self.downPin = downPin
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.upPin = upPin

    def downCtrl(self, value):
        """最下面舵机"""
        downCenter = 375
        downMax = 600
        downMin = 150
        # 左转
        print "robotArm down value:", value
        if value < 0:
            pwm_value = downCenter - ((-value) / 100.0) * (downCenter - downMin)
            self.pca_pwm.set_pwm(self.downPin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            # self.pca_pwm.set_pwm(self.downPin, 0, 0)
        # 右转
        elif value > 0:
            pwm_value = (value / 100.0) * (downMax - downCenter) + downCenter
            self.pca_pwm.set_pwm(self.downPin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            # self.pca_pwm.set_pwm(self.downPin, 0, 0)
        # 归位
        else:
            self.pca_pwm.set_pwm(self.downPin, 0, downCenter)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.downPin, 0, 0)

    def upCtrl(self, value):
        """最上面舵机"""
        upCenter = 375
        upMax = 600
        upMin = 50
        # 左转
        print "robotArm up value:", value
        if value < -10:
            pwm_value = upCenter - ((-value) / 100.0) * (upCenter - upMin)
            self.pca_pwm.set_pwm(self.upPin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            #     self.pca_pwm.set_pwm(self.upPin, 0, 0)
            # # 右转
            # elif value > 0:
            #     pwm_value = (value / 100.0) * (upMax - upCenter) + upCenter
            #     self.pca_pwm.set_pwm(self.upPin, 0, int(pwm_value))
            #     time.sleep(self.servo_angle - self.servo_Dvalue)
            #     self.pca_pwm.set_pwm(self.upPin, 0, 0)
            # # 归位
            # else:
            #     self.pca_pwm.set_pwm(self.upPin, 0, upCenter)
            #     time.sleep(self.servo_angle - self.servo_Dvalue)
            #     self.pca_pwm.set_pwm(self.upPin, 0, 0)

    def leftCtrl(self, value):
        """左边舵机"""
        leftCenter = 375
        leftMax = 600
        leftMin = 150
        # 左转
        print "robotArm left value:", value
        if value < 0:
            pwm_value = leftCenter - ((-value) / 100.0) * (leftCenter - leftMin)
            self.pca_pwm.set_pwm(self.leftPin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            # self.pca_pwm.set_pwm(self.leftPin, 0, 0)
        # 右转
        elif value > 0:
            pwm_value = (value / 100.0) * (leftMax - leftCenter) + leftCenter
            self.pca_pwm.set_pwm(self.leftPin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            # self.pca_pwm.set_pwm(self.leftPin, 0, 0)
        # 归位
        else:
            self.pca_pwm.set_pwm(self.leftPin, 0, leftCenter)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.leftPin, 0, 0)

    def rightCtrl(self, value):
        """右边舵机"""
        rightCenter = 375
        rightMax = 600
        rightMin = 150
        # 左转
        print "robotArm right value:", value
        if value < 0:
            pwm_value = rightCenter - ((-value) / 100.0) * (rightCenter - rightMin)
            self.pca_pwm.set_pwm(self.rightPin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            # self.pca_pwm.set_pwm(self.rightPin, 0, 0)
        # 右转
        elif value > 0:
            pwm_value = (value / 100.0) * (rightMax - rightCenter) + rightCenter
            self.pca_pwm.set_pwm(self.rightPin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            # self.pca_pwm.set_pwm(self.rightPin, 0, 0)
        # 归位
        else:
            self.pca_pwm.set_pwm(self.rightPin, 0, rightCenter)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            self.pca_pwm.set_pwm(self.rightPin, 0, 0)

    def clean(self):
        self.pca_pwm.set_pwm(self.upPin, 0, 0)
        self.pca_pwm.set_pwm(self.downPin, 0, 0)
        self.pca_pwm.set_pwm(self.leftPin, 0, 0)
        self.pca_pwm.set_pwm(self.rightPin, 0, 0)
if __name__ == "__main__":
    robotArmCtrl = RobotArmCtrl(3, 4, 4, 6)
