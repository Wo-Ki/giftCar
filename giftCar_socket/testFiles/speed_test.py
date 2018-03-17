# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/1/14 16:01


from __future__ import division
import RPi.GPIO as GPIO
import time, sys, math
import threading

wheelRAPin = 35  # 24
wheelRBPin = 18  # 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(wheelRAPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(wheelRBPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

wheelRCount = 0

wheelRADir = True
wheelRBDir = True

lock = threading.Lock()


def countFunc(channel):
    global wheelRCount
    if GPIO.event_detected(wheelRAPin) or GPIO.event_detected(wheelRBPin):
        while lock.acquire():
            wheelRCount += 1
            # print "count:", wheelRCount
            lock.release()


GPIO.add_event_detect(wheelRBPin, GPIO.BOTH, callback=countFunc)  # 在引脚上添加上升临界值检测再回调
GPIO.add_event_detect(wheelRAPin, GPIO.BOTH, callback=countFunc)
print("****test begin****")


def speed():
    global wheelRCount, timer
    radiusSpeed = (wheelRCount / 520.0 * (2 * math.pi)) * 2
    if not wheelRADir and radiusSpeed != 0:
        radiusSpeed = -1 * radiusSpeed
    print("speed radius A: %.2f rad/s" % radiusSpeed)
    print("speed A: %.2f m/s" % (radiusSpeed * 0.03))
    while lock.acquire():
        wheelRCount = 0
        lock.release()
    timer = threading.Timer(0.5, speed)
    timer.start()


timer = threading.Timer(0.5, speed)
timer.start()

lastTime = 0.0

while True:
    if lastTime == 0 or time.time() - lastTime >= 0.5:
        lastTime = time.time()
        # print "out"
