# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/3/25 19:08

from . import *


class BaseCarCtrl(object):
    """初始化"""
    # 设置舵机活动范围
    servo_min = 200  # Min pulse length out of 4096
    servo_center = 300
    servo_max = 400  # Max pulse length out of 4096
    servo_angle = 0.03  # sleep时间，值越大，一次的转动幅度越大
    servo_Dvalue = 0.01  # 控制左右旋转产生的误差

    def __init__(self, IN1, IN2, IN3, IN4, dir_pin):
        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4
        self.dir_pin = dir_pin

        gpio.setmode(gpio.BOARD)

        gpio.setup(self.IN1, gpio.OUT)
        gpio.setup(self.IN2, gpio.OUT)
        gpio.setup(self.IN3, gpio.OUT)
        gpio.setup(self.IN4, gpio.OUT)

        hz = 100
        self.in1_hz = gpio.PWM(self.IN1, hz)
        self.in2_hz = gpio.PWM(self.IN2, hz)
        self.in3_hz = gpio.PWM(self.IN3, hz)
        self.in4_hz = gpio.PWM(self.IN4, hz)
        self.in1_hz.start(0)
        self.in2_hz.start(0)
        self.in3_hz.start(0)
        self.in4_hz.start(0)

        self.pca_pwm = Adafruit_PCA9685.PCA9685()
        self.pca_pwm.set_pwm_freq(65)
        # 初始归位方向轮
        self.pca_pwm.set_pwm(self.dir_pin, 0, self.servo_center)
        time.sleep(self.servo_angle - self.servo_Dvalue)
        self.pca_pwm.set_pwm(self.dir_pin, 0, 0)

    def left_wheel(self, value):
        """左轮的pwm控制"""
        # 后退
        if value > 0:
            if value > 100:
                value = 100
            self.in1_hz.ChangeDutyCycle(100 - value)
            self.in2_hz.ChangeDutyCycle(100)

        # 前进
        elif value < 0:
            if value < -100:
                value = -100
            self.in1_hz.ChangeDutyCycle(-value)
            self.in2_hz.ChangeDutyCycle(0)
        # 停止
        else:
            self.in1_hz.ChangeDutyCycle(0)
            time.sleep(0.01)
            self.in2_hz.ChangeDutyCycle(0)
            time.sleep(0.01)

    def right_wheel(self, value):
        """右轮的pwm控制"""
        # 后退
        if value > 0:
            if value > 100:
                value = 100
            self.in3_hz.ChangeDutyCycle(100 - value)
            self.in4_hz.ChangeDutyCycle(100)
        # 前进
        elif value < 0:
            if value < -100:
                value = -100
            self.in3_hz.ChangeDutyCycle(-value)
            self.in4_hz.ChangeDutyCycle(0)
            # 停止
        else:
            self.in3_hz.ChangeDutyCycle(0)
            self.in4_hz.ChangeDutyCycle(0)

    def dir_ctrl(self, value):
        """方向轮的pwm控制"""
        # 左转
        if value < 0:
            pwm_value = self.servo_center - ((-value) / 100.0) * (self.servo_center - self.servo_min)
            self.pca_pwm.set_pwm(self.dir_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            # self.pca_pwm.set_pwm(self.dir_pin, 0, 0)
        # 右转
        elif value > 0:
            pwm_value = (value / 100.0) * (self.servo_max - self.servo_center) + self.servo_center
            self.pca_pwm.set_pwm(self.dir_pin, 0, int(pwm_value))
            time.sleep(self.servo_angle - self.servo_Dvalue)
            # self.pca_pwm.set_pwm(self.dir_pin, 0, 0)
        # 归位
        else:
            self.pca_pwm.set_pwm(self.dir_pin, 0, self.servo_center)
            time.sleep(self.servo_angle - self.servo_Dvalue)
            # self.pca_pwm.set_pwm(self.dir_pin, 0, 0)

    def stop(self):
        self.pca_pwm.set_pwm(self.dir_pin, 0, self.servo_center)
        time.sleep(self.servo_angle - self.servo_Dvalue)
        self.in3_hz.ChangeDutyCycle(0)
        self.in4_hz.ChangeDutyCycle(0)
        self.in1_hz.ChangeDutyCycle(0)
        self.in2_hz.ChangeDutyCycle(0)
