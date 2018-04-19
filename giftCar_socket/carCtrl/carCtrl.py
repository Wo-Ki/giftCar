# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/4/5 09:59

from . import *
import threading
from .baseCarCtrl import BaseCarCtrl


class CarCtrl(BaseCarCtrl):
    speed_l_count = 0
    speed_r_count = 0
    speed_l_pre = 0.0
    speed_r_pre = 0.0
    speed_l_real = 0.0  # 线速度 m/s
    speed_r_real = 0.0  # 线速度 m/s
    origin_wheel_value = 0

    avoid_up_left = False
    avoid_up_right = False
    avoid_down_left = False
    avoid_down_right = False

    avoid_mode = True

    client_socket = None

    def __init__(self, IN1, IN2, IN3, IN4, dir_pin, avoid_down_left_pin, avoid_down_right_pin, speed_left_pin,
                 speed_right_pin):
        super(CarCtrl, self).__init__(IN1, IN2, IN3, IN4, dir_pin)
        self.avoid_down_left_pin = avoid_down_left_pin
        self.avoid_down_right_pin = avoid_down_right_pin
        self.speed_left_pin = speed_left_pin
        self.speed_right_pin = speed_right_pin
        gpio.setup(avoid_down_left_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(avoid_down_right_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(avoid_down_left_pin, gpio.BOTH, callback=self.avoid_down_left_changed)
        gpio.add_event_detect(avoid_down_right_pin, gpio.BOTH, callback=self.avoid_down_right_changed)

        gpio.setup(speed_left_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(speed_right_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(speed_left_pin, gpio.RISING, callback=self.speed_left_func)
        gpio.add_event_detect(speed_right_pin, gpio.RISING, callback=self.speed_right_func)

        timer = threading.Timer(0.5, self.get_both_speed)
        timer.start()

    @staticmethod
    def set_client_socket(client_socket):
        """当连接上客户端，设置socket，以便速度和避障上传"""
        CarCtrl.client_socket = client_socket

    def set_speed(self, value):
        """从云端下发的原始数据"""
        self.origin_wheel_value = value
        # if value > 0 and self.avoid_down_left is False and self.avoid_down_right is False:
        self.left_wheel(value)
        self.right_wheel(value)

    # def avoid_up_left_changed(self, channel):
    #     if gpio.event_detected(self.avoid_up_left_pin):
    #         if gpio.input(self.avoid_up_left_pin) == gpio.LOW:
    #             self.avoid_up_left = True
    #             if self.origin_wheel_value < 0:
    #                 self.set_speed(0)
    #                 # print "self.avoid_up_left:", self.avoid_up_left
    #         else:
    #             self.avoid_up_left = False
    #             # print "self.avoid_up_left:", self.avoid_up_left

    def avoid_down_left_changed(self, channel):
        if gpio.event_detected(self.avoid_down_left_pin):
            if gpio.input(self.avoid_down_left_pin) == gpio.LOW:
                self.avoid_down_left = True
                if self.origin_wheel_value > 0:
                    self.set_speed(0)
                self.send_avoid_status("dl", 1)
            else:
                self.avoid_down_left = False
                self.send_avoid_status("dl", 0)

    def avoid_down_right_changed(self, channel):
        if gpio.event_detected(self.avoid_down_right_pin):
            if gpio.input(self.avoid_down_right_pin) == gpio.LOW:
                self.avoid_down_right = True
                if self.origin_wheel_value > 0:
                    self.set_speed(0)
                self.send_avoid_status("dr", 1)
            else:
                self.avoid_down_right = False
                self.send_avoid_status("dr", 0)

    def send_avoid_status(self, which, value):
        """向云端发送障碍物状态"""
        if self.client_socket:
            s = {"M": "update", "K": "avoid", "V": {"W": which, "V": value}}
            self.client_socket.send(json.dumps(s).encode("utf-8"))
            time.sleep(0.05)

    def speed_left_func(self, channel):
        if gpio.event_detected(self.speed_left_pin):
            self.speed_l_count += 1

    def speed_right_func(self, channel):
        if gpio.event_detected(self.speed_right_pin):
            self.speed_r_count += 1

    def get_both_speed(self):
        """定时测速"""
        self.speed_l_pre = self.speed_l_count
        self.speed_r_pre = self.speed_r_count
        # print "speed_l_pre:", self.speed_l_pre
        # print "speed_r_pre:", self.speed_r_pre
        self.speed_l_count = 0
        self.speed_r_count = 0
        self.real_speed()
        timer = threading.Timer(0.5, self.get_both_speed)
        timer.start()

    def real_speed(self):
        """向上位机上传真是速度"""
        self.speed_l_real = (self.speed_l_pre / 130.0 * (2 * math.pi)) * 2 * 0.03
        self.speed_r_real = (self.speed_r_pre / 130.0 * (2 * math.pi)) * 2 * 0.03
        if self.client_socket:
            average_speed = (self.speed_l_real + self.speed_r_real) / 2.0
            s = {"M": "update", "K": "speed", "V": average_speed}
            self.client_socket.send(json.dumps(s).encode("utf-8"))
            time.sleep(0.05)
