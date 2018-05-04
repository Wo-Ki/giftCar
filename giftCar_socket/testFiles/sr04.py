# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/5/4 09:08


import RPi.GPIO as GPIO
import time


echo = 33
trig = 35

def checkdist():
    # 发出触发信号
    GPIO.output(trig, GPIO.HIGH)
    # 保持10us以上（我选择15us）
    time.sleep(0.000015)
    GPIO.output(trig, GPIO.LOW)

    while not GPIO.input(echo):
        pass
    # 发现高电平时开时计时
    t1 = time.time()
    while GPIO.input(echo):
        if time.time() - t1 >= 0.0588235:  # 超过10米终止,来回共20米的时间
            return -1
    # 高电平结束停止计时
    t2 = time.time()
    # 返回距离，单位为米
    return (t2 - t1) * 340 / 2


GPIO.setmode(GPIO.BOARD)
# 第3号针，GPIO2
GPIO.setup(trig, GPIO.OUT, initial=GPIO.LOW)
# 第5号针，GPIO3
GPIO.setup(echo, GPIO.IN)

time.sleep(2)
try:
    while True:
        print("Distance: %0.2f m" % checkdist())
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
