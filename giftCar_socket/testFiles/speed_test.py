# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/1/14 16:01


from __future__ import division
import RPi.GPIO as GPIO
import time, sys, math

wheelRAPin = 35
wheelRBPin = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(wheelRAPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(wheelRBPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

wheelRACount = 0
wheelRBCount = 0
wheelRCount = 0


wheelRADir = True
wheelRBDir = True


def wheelRAFunc(channel):  # 边缘检测回调函数，详情在参见链接中
    global wheelRACount, wheelRADir  # 设置为全局变量
    if GPIO.event_detected(wheelRAPin):  # 检测到一个脉冲则脉冲数加1
        wheelRACount = wheelRACount + 1
        if GPIO.input(wheelRBPin) == GPIO.HIGH:
            wheelRADir = True
        else:
            wheelRADir = False
    # print "counter RA:", wheelRACount


def wheelRBFunc(channel):  # 这里的channel和channel1无须赋确定值，但笔者测试过，不能不写
    global wheelRBCount
    if GPIO.event_detected(wheelRBPin):
        wheelRBCount = wheelRBCount + 1

    # print "counter RB:", wheelRBCount

def countFunc(channel):
    global wheelRCount
    if GPIO.event_detected(wheelRAPin) or GPIO.event_detected(wheelRBPin):
        wheelRCount += 1
    print "count:", wheelRCount


# GPIO.add_event_detect(wheelRBPin, GPIO.RISING, callback=wheelRBFunc)  # 在引脚上添加上升临界值检测再回调
# GPIO.add_event_detect(wheelRAPin, GPIO.RISING, callback=wheelRAFunc)
GPIO.add_event_detect(wheelRBPin, GPIO.BOTH, callback=countFunc)  # 在引脚上添加上升临界值检测再回调
GPIO.add_event_detect(wheelRAPin, GPIO.BOTH, callback=countFunc)
print "****test begin****"

lastTime = 0.0

while True:
    if lastTime == 0 or time.time() - lastTime >= 0.5:
        lastTime = time.time()
        radiusSpeed = (wheelRACount / 150 * 2 * math.pi) * 2
        if not wheelRADir and radiusSpeed != 0:
            radiusSpeed = -1 * radiusSpeed
        print "speed radius A: %.2f rad/s" % radiusSpeed
        print "speed A: %.2f m/s" % (radiusSpeed * 0.03)
        wheelRACount = 0

