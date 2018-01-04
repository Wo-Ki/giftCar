# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/31 15:05

import socket
import json
import car_pwm_ctrl
import robotArmCtrl


host = "192.168.100.2"
port = 8989


def handle_client(client_socket, client_address):
    """处理客户端"""
    client_socket.send("OK\r\n")
    while True:
        try:
            request_data = client_socket.recv(1024)
            if request_data:
                print "request_data:", request_data
                try:
                    json_datas = request_data.split(",")
                    for json_data in json_datas:
                        json_data = json.loads(json_data)
                        if json_data.get("UD") is not None:
                            car_pwm_ctrl.left_wheel(int(json_data.get("UD")))
                            car_pwm_ctrl.right_wheel(int(json_data.get("UD")))
                        if json_data.get("LR") is not None:
                            car_pwm_ctrl.dir_ctrl(int(json_data.get("LR")))
                        if json_data.get("YH") is not None:
                            car_pwm_ctrl.yh_ctrl(int(json_data.get("YH")))
                        if json_data.get("YV") is not None:
                            car_pwm_ctrl.yv_ctrl(int(json_data.get("YV")))
                        if json_data.get("AU") is not None:
                            robotArmCtrl.upCtrl(int(json_data.get("AU")))
                        if json_data.get("AD") is not None:
                            robotArmCtrl.downCtrl(int(json_data.get("AD")))
                        if json_data.get("AL") is not None:
                            robotArmCtrl.leftCtrl(int(json_data.get("AL")))
                        if json_data.get("AR") is not None:
                            robotArmCtrl.rightCtrl(int(json_data.get("AR")))
                except:
                    pass
            else:
                print "[%s, %s] : disconnect" % client_address
                client_socket.close()
                return
        except Exception, e:
            print e
            print "[%s, %s] : disconnect" % client_address
            client_socket.close()
            return


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.bind((host, port))
    server_socket.listen(3)

    car_pwm_ctrl = car_pwm_ctrl.Car_pwm_ctrl(13, 12, 15, 16, 0, 1, 2)
    robotArmCtrl = robotArmCtrl.RobotArmCtrl(3, 4, 5, 6)
    print "******Server Online*****"
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print "*" * 30
            print "[%s, %s] : connected" % client_address
            handle_client(client_socket, client_address)
    except KeyboardInterrupt:
        print "******Server Offline*****"
        client_socket.close()
        server_socket.close()
