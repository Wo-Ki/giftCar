# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/4/5 09:27


class JsonAnalysis(object):
    """处理上位机下发的json数据"""

    def __init__(self, servoCtrl, carCtrl, robotArmCtrl):
        self.servoCtrl = servoCtrl
        self.carCtrl = carCtrl
        self.robotArmCtrl = robotArmCtrl

    def analysis(self, json_data):
        """处理json数据"""
        if json_data.get("UD") is not None:
            # self.carCtrl.left_wheel(int(json_data.get("UD")))
            # self.carCtrl.right_wheel(int(json_data.get("UD")))
            self.carCtrl.set_speed(int(json_data.get("UD")))
        if json_data.get("LR") is not None:
            self.carCtrl.dir_ctrl(int(json_data.get("LR")))
        if json_data.get("YH") is not None:
            self.servoCtrl.yh_ctrl(int(json_data.get("YH")))
        if json_data.get("YV") is not None:
            self.servoCtrl.yv_ctrl(int(json_data.get("YV")))
        if json_data.get("AU") is not None:
            self.robotArmCtrl.upCtrl(int(json_data.get("AU")))
        if json_data.get("AD") is not None:
            self.robotArmCtrl.downCtrl(int(json_data.get("AD")))
        if json_data.get("AL") is not None:
            self.robotArmCtrl.leftCtrl(int(json_data.get("AL")))
        if json_data.get("AR") is not None:
            self.robotArmCtrl.rightCtrl(int(json_data.get("AR")))
        if json_data.get("AC") is not None:
            self.robotArmCtrl.clean()
        if json_data.get("M") is not None:
            if json_data["M"] == 'stop':
                self.carCtrl.stop()
            elif json_data["M"] == 'avoid':
                if json_data["V"] == 'on':
                    self.carCtrl.set_avoid_mode(True)
                elif json_data["V"] == 'off':
                    self.carCtrl.set_avoid_mode(False)

