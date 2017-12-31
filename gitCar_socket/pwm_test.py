# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/31 15:22

import RPi.GPIO as gpio
import time, sys

# 我用的第12个引脚
pin = 12
gpio.setmode(gpio.BOARD)
gpio.setup(pin, gpio.OUT)
# 频率设置为400Hz
p = gpio.PWM(pin, 400)
p.start(0)
# 占空比从10开始，逐渐加到90
dc = 10
for i in range(40):
    dc += 2
    print 'dc:', dc
    p.ChangeDutyCycle(dc)
    time.sleep(0.3);
p.stop()
gpio.cleanup()
