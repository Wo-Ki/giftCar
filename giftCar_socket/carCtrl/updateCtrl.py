# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/4/7 22:21

import json
from .sensorCtrl import SensorCtrl
from . import *


class UpdateCtrl(SensorCtrl):
    """上传数据到云端"""

    def __init__(self, client_socket, dth11_pin):
        super(UpdateCtrl, self).__init__(dth11_pin)
        self.client_socket = client_socket

    def updateDHT11(self):
        hum, tem = self.get_dht11_data()
        s = {"M": "update", "K": "dht11", "V": {"hum": hum, 'tem': tem}}
        self.client_socket.send(bytes(json.dumps(s)))
        time.sleep(0.1)

    def updateMpu9250(self):
        gyro_xout, gyro_yout, gyro_zout = self.get_gyro_data()
        s = {"M": "update", "K": "gyro", "V": {"x": gyro_xout, 'y': gyro_yout, "z": gyro_zout}}
        self.client_socket.send(bytes(json.dumps(s)))
        time.sleep(0.05)

        accel_xout, accel_yout, accel_zout = self.get_accelerometer_data()
        s = {"M": "update", "K": "accel", "V": {"x": accel_xout, 'y': accel_yout, "z": accel_zout}}
        self.client_socket.send(bytes(json.dumps(s)))
        time.sleep(0.05)
