# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/5/18 21:38

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, N=0)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((30, 40), "Hello Wo-Ki", fill="white")

while True:
    pass