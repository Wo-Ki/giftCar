# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/4/8 15:54

from . import *
import Adafruit_DHT
import smbus


class SensorCtrl(object):
    """获取传感器数据"""
    dht11 = Adafruit_DHT.DHT11

    # Power management registers
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c
    bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
    address = 0x68  # This is the address value read via the i2cdetect command
    address2 = 0x0C

    def __init__(self, dht11_pin):
        self.dht11_pin = dht11_pin
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 1)

    # 以下为dth11
    def get_dht11_data(self):
        """获取dht11数据"""
        while 1:
            try:
                (humidity, temperature) = Adafruit_DHT.read_retry(self.dht11, self.dht11_pin)
                if humidity is None:
                    humidity = -1
                if temperature is None:
                    temperature = -1
            except RuntimeError as e:
                print("get_dht11_data error:", e)
                (humidity, temperature) = (-1, -1)
            yield humidity, temperature

    # 以下为mpu9250
    def read_byte(self,device_addr, adr):
        return self.bus.read_byte_data(device_addr, adr)

    def read_word(self,device_addr, adr):
        high = self.bus.read_byte_data(device_addr, adr)
        low = self.bus.read_byte_data(device_addr, adr + 1)
        val = (high << 8) + low
        return val

    def read_word_2c(self,device_addr, adr):
        val = self.read_word(device_addr, adr)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_rotation(self):
        x, y, z = self.get_accelerometer_data().__next__()
        x /= 16384.0
        y /= 16384.0
        z /= 16384.0
        x_radians = math.atan2(y, self.dist(x, z))
        y_radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(x_radians), -math.degrees(y_radians)

    def get_gyro_data(self):
        while 1:
            gyro_xout = self.read_word_2c(self.address, 0x43) / 131.0  # ±250
            gyro_yout = self.read_word_2c(self.address, 0x45) / 131.0
            gyro_zout = self.read_word_2c(self.address, 0x47) / 131.0
            yield gyro_xout, gyro_yout, gyro_zout

    def get_accelerometer_data(self):
        # accel_xout = self.read_word_2c(self.address, 0x3b) / 16384.0
        # accel_yout = self.read_word_2c(self.address, 0x3d) / 16384.0
        # accel_zout = self.read_word_2c(self.address, 0x3f) / 16384.0
        while 1:
            accel_xout = self.read_word_2c(self.address, 0x3b)
            accel_yout = self.read_word_2c(self.address, 0x3d)
            accel_zout = self.read_word_2c(self.address, 0x3f)
            yield accel_xout, accel_yout, accel_zout

    def get_magnetometer_data(self):
        while 1:
            self.bus.write_byte_data(self.address, 0x37, 0x02)
            self.bus.write_byte_data(self.address2, 0x0A, 0x01)
            time.sleep(0.02)
            mag_xout = self.read_word_2c(self.address2, 0x04)
            mag_yout = self.read_word_2c(self.address2, 0x06)
            mag_zout = self.read_word_2c(self.address2, 0x08)
            yield mag_xout, mag_yout, mag_zout