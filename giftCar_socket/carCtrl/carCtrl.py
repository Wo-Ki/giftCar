# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/4/5 09:59

from . import *
from .baseCarCtrl import BaseCarCtrl
from .radarCtrl import RadarCtrl
from ctypes import *


class CarCtrl(BaseCarCtrl):
    speed_r_last_count = 0
    speed_r_pre = 0.0  # 原始条边沿数表示的速度,负数向前
    speed_r_real = 0.0  # 线速度 m/s
    origin_wheel_value = 0

    avoid_up_left = False
    avoid_up_right = False
    avoid_down_left = False
    avoid_down_right = False

    avoid_mode = True  # 避障模式默认开启

    client_socket = None

    def __init__(self, lock, IN1, IN2, IN3, IN4, dir_pin, avoid_up_left_pin, avoid_up_right_pin):
        # super(CarCtrl, self).__init__(IN1, IN2, IN3, IN4, dir_pin)
        super(CarCtrl, self).__init__(IN1, IN2, IN3, IN4, dir_pin)
        # super(BaseCarCtrl, self).__init__(7, 33, 35)
        self.lock = lock
        self.radarCtrl = RadarCtrl(7, 33, 35)
        self.avoid_up_left_pin = avoid_up_left_pin
        self.avoid_up_right_pin = avoid_up_right_pin
        gpio.setup(avoid_up_left_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(avoid_up_right_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        self.avoid_up_left = not gpio.input(self.avoid_up_left_pin)
        self.avoid_up_right = not gpio.input(self.avoid_up_right_pin)
        print("up left:", self.avoid_up_left)
        print("up right:", self.avoid_up_right)
        gpio.add_event_detect(avoid_up_left_pin, gpio.BOTH, callback=self.avoid_up_left_changed)
        gpio.add_event_detect(avoid_up_right_pin, gpio.BOTH, callback=self.avoid_up_right_changed)

        self.lib = cdll.LoadLibrary("./carCtrl/right_speed.so")
        self.lib.main()
        right_speed_timer = threading.Timer(0.2, self.speed_right_func)  # 从C文件0.2s读取速度
        right_speed_timer.start()

        timer_sr04 = threading.Timer(0.02, self.send_sr04)
        timer_sr04.start()

    @staticmethod
    def set_client_socket(client_socket):
        """当连接上客户端，设置socket，以便速度和避障上传"""
        CarCtrl.client_socket = client_socket

    @staticmethod
    def set_avoid_mode(value):
        CarCtrl.avoid_mode = value

    def set_speed(self, value):
        """从云端下发的原始数据 -100 ~ 100"""
        print("avoid mode:", self.avoid_mode)
        self.origin_wheel_value = value
        if self.avoid_mode:  # 开启避障模式
            if (value > 0 and self.avoid_down_left is False and self.avoid_down_right is False) or (
                                value < 0 and self.avoid_up_left is False and self.avoid_up_right is False) or value == 0:
                self.left_wheel(value)
                self.right_wheel(value)
        else:
            self.left_wheel(value)
            self.right_wheel(value)

    def avoid_up_left_changed(self, channel):
        """避障中断"""
        if gpio.event_detected(self.avoid_up_left_pin):
            if gpio.input(self.avoid_up_left_pin) == gpio.LOW:
                self.avoid_up_left = True
                if self.origin_wheel_value < 0:
                    if self.avoid_mode:  # 开启避障时，紧急制动
                        self.break_now()
                self.send_avoid_status("ul", 1)
            else:
                self.avoid_up_left = False
                self.send_avoid_status("ul", 0)

    def avoid_up_right_changed(self, channel):
        if gpio.event_detected(self.avoid_up_right_pin):
            if gpio.input(self.avoid_up_right_pin) == gpio.LOW:
                self.avoid_up_right = True
                if self.origin_wheel_value < 0:
                    if self.avoid_mode:
                        self.break_now()
                self.send_avoid_status("ur", 1)
            else:
                self.avoid_up_right = False
                self.send_avoid_status("ur", 0)

    def avoid_down_left_changed(self, channel):
        """避障中断"""
        if gpio.event_detected(self.avoid_down_left_pin):
            if gpio.input(self.avoid_down_left_pin) == gpio.LOW:
                self.avoid_down_left = True
                if self.origin_wheel_value > 0:
                    if self.avoid_mode:  # 开启避障时，紧急制动
                        self.break_now()
                self.send_avoid_status("dl", 1)
            else:
                self.avoid_down_left = False
                self.send_avoid_status("dl", 0)

    def avoid_down_right_changed(self, channel):
        if gpio.event_detected(self.avoid_down_right_pin):
            if gpio.input(self.avoid_down_right_pin) == gpio.LOW:
                self.avoid_down_right = True
                if self.origin_wheel_value > 0:
                    if self.avoid_mode:
                        self.break_now()
                self.send_avoid_status("dr", 1)
            else:
                self.avoid_down_right = False
                self.send_avoid_status("dr", 0)

    def send_avoid_status(self, which, value):
        """向云端发送障碍物状态"""
        if self.client_socket:
            s = {"M": "update", "K": "avoid", "V": {"W": which, "V": value}}
            if self.lock.acquire():
                self.client_socket.send(json.dumps(s).encode("utf-8"))
                time.sleep(0.01)
                self.lock.release()
                # time.sleep(0.05)

    def break_now(self):
        """制动"""

        while abs(self.speed_r_pre) != 0:
            k = -self.speed_r_pre * 0.3
            print("K:", k)
            if self.speed_r_pre < 0:  # 当前向前运动
                self.left_wheel(k)
                self.right_wheel(k)
                time.sleep(0.02)
                # k -= abs(self.speed_r_pre) * 0.02
            elif self.speed_r_pre > 0:  # 当前向后运动
                self.left_wheel(k)
                self.right_wheel(k)
                time.sleep(0.02)
                # k += abs(self.speed_r_pre) * 0.02

        self.stop()

    def speed_left_func(self):
        pass

    def speed_right_func(self):
        """从C文件0.2s读取速度，负数为前进"""
        count = self.lib.returnRightCount()
        self.speed_r_pre = count - self.speed_r_last_count
        self.speed_r_last_count = count
        self.work_real_speed()
        right_speed_timer = threading.Timer(0.2, self.speed_right_func)
        right_speed_timer.start()

    def work_real_speed(self):
        """求出真实线速度，向上位机上传真是速度"""
        # self.speed_l_real = (self.speed_l_pre / 130.0 * (2 * math.pi)) * 2 * 0.03
        self.speed_r_real = (self.speed_r_pre / 260.0 * (2 * math.pi)) * 5 * 0.03  # 线速度
        if self.client_socket:
            s = {"M": "update", "K": "speed", "V": self.speed_r_real}
            while self.lock.acquire():
                self.client_socket.send(json.dumps(s).encode("utf-8"))
                time.sleep(0.01)
                self.lock.release()

    def send_sr04(self):
        """发送sr04的数据，距离和角度"""
        angle, distance = self.radarCtrl.get_servo_and_distance()
        if self.client_socket:
            s = {"M": "update", "K": "sr04", "V": [angle, distance]}
            if self.lock.acquire():
                self.client_socket.send(json.dumps(s).encode("utf-8"))
                time.sleep(0.01)
                self.lock.release()
                # time.sleep(0.02)
        # print("angle and distance:", angle, distance)
        timer_sr04 = threading.Timer(0.02, self.send_sr04)
        timer_sr04.start()


if __name__ == "__main__":
    carCtrl = CarCtrl(13, 12, 15, 16, 0, 7, 32)
    carCtrl.stop()
