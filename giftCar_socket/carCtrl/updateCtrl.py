# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/4/7 22:21

import json
from .sensorCtrl import SensorCtrl
from . import *


class UpdateCtrl(SensorCtrl):
    """上传数据到云端"""

    def __init__(self, lock, client_socket, dth11_pin):
        super(UpdateCtrl, self).__init__(dth11_pin)
        self.lock = lock
        self.client_socket = client_socket
        # 生成器对象
        self.get_dht11_data_generator = self.get_dht11_data()
        self.get_gyro_data_generator = self.get_gyro_data()
        self.get_accelerometer_data_generator = self.get_accelerometer_data()

    def updateDHT11(self):
        time1 = time.time()
        hum, tem = self.get_dht11_data_generator.next()
        print("hum:", hum, "tem:", tem)
        s = {"M": "update", "K": "dht11", "V": {"hum": hum, 'tem': tem}}
        print("dht11 time:", time.time() - time1)
        if self.lock.acquire():
            self.client_socket.send(json.dumps(s).encode("utf-8"))
            time.sleep(0.01)
            self.lock.release()
        # time.sleep(0.1)

    def updateMpu9250(self):
        gyro_xout, gyro_yout, gyro_zout = self.get_gyro_data_generator.next()
        accel_xout, accel_yout, accel_zout = self.get_accelerometer_data_generator.next()
        s = {"M": "update", "K": "mpu9250",
             "V": {"gx": gyro_xout, 'gy': gyro_yout, "gz": gyro_zout, "ax": accel_xout, 'ay': accel_yout,
                   "az": accel_zout}}
        if self.lock.acquire():
            self.client_socket.send(json.dumps(s).encode("utf-8"))
            time.sleep(0.01)
            self.lock.release()
        # time.sleep(0.05)
