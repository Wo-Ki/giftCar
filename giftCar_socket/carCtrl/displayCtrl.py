# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/5/4 15:37

from . import *
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class DisplayCtrl(object):
    """控制12864显示器"""

    def __init__(self, rst=0):
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=-1)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()

        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, self.width, self.height), outline=1, fill=1)

    def hello(self):
        font = ImageFont.truetype(size=30)
        self.draw.text((0, 0), "Hello", font=font, fill=255)
