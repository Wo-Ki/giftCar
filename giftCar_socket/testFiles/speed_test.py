# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/1/14 16:01

import RPi.GPIO as GPIO
import time, sys

wheelRAPin = 35
wheelRBPin = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(wheelRBPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(wheelRAPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
wheelRACount = 0
wheelRBCount = 0


def wheelRAFunc(channel):  # 边缘检测回调函数，详情在参见链接中
    global wheelRACount  # 设置为全局变量
    if GPIO.event_detected(wheelRAPin):  # 检测到一个脉冲则脉冲数加1
        counter = wheelRAPin + 1
    print "counter RA:", counter


def wheelRBFunc(channel):  # 这里的channel和channel1无须赋确定值，但笔者测试过，不能不写
    global wheelRBCount
    if GPIO.event_detected(wheelRBPin):
        counter = wheelRBCount + 1
    print "counter RB:", counter


GPIO.add_event_detect(wheelRBPin, GPIO.RISING, callback=wheelRBFunc)  # 在引脚上添加上升临界值检测再回调
GPIO.add_event_detect(wheelRAPin, GPIO.RISING, callback=wheelRAFunc)

print "****test begin****"

while True:
    pass
