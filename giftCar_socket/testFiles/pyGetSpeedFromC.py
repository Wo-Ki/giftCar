# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/4/22 22:08

from ctypes import *
import time

lib = cdll.LoadLibrary("./speed.so")
lib.main()

lastCount = 0
while 1:
    count = lib.returnCount()
    print("count:", count)
    speed = count - lastCount
    print("speed:", speed)
    lastCount = count
    time.sleep(0.5)
