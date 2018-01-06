# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/31 15:05

import socket
import json
import car_pwm_ctrl
import robotArmCtrl
from multiprocessing import Process
import requests
from camera_pi import Camera

host = "192.168.100.2"
port = 8989


def gen(camera):
    """Video streaming genreator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\b'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def handle_client(client_socket, client_address):
    """处理客户端"""
    client_socket.send("OK\r\n")
    while True:
        try:
            request_data = client_socket.recv(1024)
            if request_data:
                print "request_data:", request_data
                if request_data.find("GET /video") != -1:
                    # 浏览器视频
                    print "Brower Linked"
                    responseStartLine = "HTTP/1.1 200 OK\r\n"
                    responseHeader = "Server: my erver\r\n"
                    responseBody = gen(Camera())
                    response = responseStartLine + responseHeader + "\r\n" + "Hello"
                    client_socket.send(bytes(response))
                    client_socket.close()
                else:
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
                            if json_data.get("AC") is not None:
                                robotArmCtrl.clean()
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
    print "***", host, port, "***"
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print "*" * 30
            print "[%s, %s] : connected" % client_address
            handle_client_process = Process(target=handle_client, args=(client_socket, client_address))
            # handle_client(client_socket, client_address)
            handle_client_process.start()
            client_socket.close()

    except KeyboardInterrupt:
        print "******Server Offline*****"
        robotArmCtrl.clean()
        client_socket.close()
        server_socket.close()
