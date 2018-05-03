# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/5/3 18:26

import RPi.GPIO as GPIO
import time

# trig = 37
#
#
# def init():
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setup(trig, GPIO.OUT, initial=GPIO.HIGH)
#     pass
#
#
# def beep(seconds):
#     GPIO.output(trig, GPIO.LOW)
#     time.sleep(seconds)
#     GPIO.output(trig, GPIO.HIGH)
#
#
# def beepBatch(seconds, timespan, counts):
#     for i in range(counts):
#         beep(seconds)
#         time.sleep(timespan)
#
#
# init()
# # beep(0.1)
# beepBatch(0.1, 0.3, 3)
#
# GPIO.cleanup()

import RPi.GPIO as GPIO
import time

PIN_NO = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_NO, GPIO.OUT)


def beep(seconds):
    GPIO.output(PIN_NO, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(PIN_NO, GPIO.LOW)


def beepAction(secs, sleepsecs, times):
    for i in range(times):
        beep(secs)
        time.sleep(sleepsecs)
