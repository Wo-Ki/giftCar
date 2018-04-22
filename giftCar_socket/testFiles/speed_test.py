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

encoder_r = 22
direction_r = 18
velocity_r = 0

GPIO.setup(encoder_r, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(direction_r, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lock = threading.Lock()


def countFunc(channel):
    global wheelRCount
    if GPIO.event_detected(wheelRAPin) or GPIO.event_detected(wheelRBPin):
        lock.acquire()
        wheelRCount += 1
        # print "count:", wheelRCount
        lock.release()


def read_encoder_r(channel):
    global velocity_r
    if GPIO.event_detected(encoder_r):
        lock.acquire()
        if GPIO.input(encoder_r) == GPIO.LOW:
            if GPIO.input(direction_r) == GPIO.LOW:
                velocity_r += 1
            else:
                velocity_r -= 1
        else:
            if GPIO.input(direction_r) == GPIO.LOW:
                velocity_r -= 1
            else:
                velocity_r += 1
        lock.release()


GPIO.add_event_detect(encoder_r, GPIO.BOTH, callback=read_encoder_r)
# GPIO.add_event_detect(wheelRBPin, GPIO.RISING, callback=countFunc)  # 在引脚上添加上升临界值检测再回调
# GPIO.add_event_detect(wheelRAPin, GPIO.BOTH, callback=countFunc)
print("****test begin****")


def speed():
    global wheelRCount, timer
    radiusSpeed = (wheelRCount / 130.0 * (2 * math.pi)) * 2
    if not wheelRADir and radiusSpeed != 0:
        radiusSpeed = -1 * radiusSpeed
    print("speed radius A: %.2f rad/s" % radiusSpeed)
    print("speed A: %.2f m/s" % (radiusSpeed * 0.03))
    lock.acquire()
    wheelRCount = 0
    lock.release()
    timer = threading.Timer(0.5, speed)
    timer.start()


def control():
    global velocity_r
    print "velocity_r:", velocity_r
    lock.acquire()
    velocity_r = 0
    lock.release()
    timer = threading.Timer(0.5, control)
    timer.start()

timer = threading.Timer(0.5, control)
timer.start()

lastTime = 0.0

while True:
    if lastTime == 0 or time.time() - lastTime >= 0.5:
        lastTime = time.time()
        # print "out"
