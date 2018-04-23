# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/4/7 08:34

# !/usr/bin/python
import smbus
import math
import time

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68  # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)
time.sleep(0.01)
# bus.write_byte_data(address, 0x37, 0x02)
# time.sleep(0.01)
bus.write_byte_data(0x0C, 0x0A, 0x01)
time.sleep(0.01)
while True:
    # print "gyro data"
    # print "---------"
    #
    # gyro_xout = read_word_2c(0x43)
    # gyro_yout = read_word_2c(0x45)
    # gyro_zout = read_word_2c(0x47)
    #
    # print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
    # print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
    # print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)
    #
    # print
    # print "accelerometer data"
    # print "------------------"
    #
    # accel_xout = read_word_2c(0x3b)
    # accel_yout = read_word_2c(0x3d)
    # accel_zout = read_word_2c(0x3f)
    #
    # accel_xout_scaled = accel_xout / 16384.0
    # accel_yout_scaled = accel_yout / 16384.0
    # accel_zout_scaled = accel_zout / 16384.0
    #
    # print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
    # print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
    # print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled
    #
    # print "x rotation: ", get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    # print "y rotation: ", get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

    print("tem data")
    print("---------")
    tem = read_word_2c(0X41)
    print("tem :", tem)

    print("RA_MAG data")
    print("---------")
    mag_xout = read_word_2c(0x04)
    mag_yout = read_word_2c(0x06)
    mag_zout = read_word_2c(0x08)
    print("mag_xout: ", mag_xout)
    print("mag_yout: ", mag_yout)
    print("mag_zout: ", mag_zout)


    time.sleep(0.5)


    # define SMPLRT_DIV                 0X19 //陀螺仪采样率典型值为0X07 1000/(1+7)=125HZ

    # define CONFIG                         0X1A //低通滤波器  典型值0x06 5hz

    # define GYRO_CONFIG                0X1B //陀螺仪测量范围 0X18 正负2000度

    # define ACCEL_CONFIG            0X1C //加速度计测量范围 0X18 正负16g

    # define ACCEL_CONFIG2           0X1D //加速度计低通滤波器 0x06 5hz

    # define PWR_MGMT_1                  0X6B//电源管理1 典型值为0x00

    # define PWR_MGMT_2                 0X6C //电源管理2 典型值为0X00



    # define WHO_AM_I                    0X75 //器件ID MPU9250默认ID为0X71

    # define USER_CTRL                   0X6A //用户配置当为0X10时使用SPI模式



    # define MPU9250_CS        PDout(3) //MPU9250片选信号

    # define I2C_ADDR                    0X68  //i2c的地址

    # define ACCEL_XOUT_H            0X3B  //加速度计输出数据

    # define ACCEL_XOUT_L            0X3C

    # define ACCEL_YOUT_H            0X3D

    # define ACCEL_YOUT_L            0X3E

    # define ACCEL_ZOUT_H            0X3F

    # define ACCEL_ZOUT_L            0X40



    # define TEMP_OUT_H               0X41  //温度计输出数据

    # define TEMP_OUT_L               0X42



    # define GYRO_XOUT_H              0X43  //陀螺仪输出数据

    # define GYRO_XOUT_L              0X44

    # define GYRO_YOUT_H              0X45

    # define GYRO_YOUT_L              0X46

    # define GYRO_ZOUT_H              0X47

    # define GYRO_ZOUT_L                 0X48
