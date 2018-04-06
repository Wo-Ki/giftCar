# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/31 15:05

import json
import socket

from carCtrl import robotArmCtrl, jsonAnalysis, carCtrl, servoCtrl

host = "0.0.0.0"
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
                        jsonCtrl.analysis(json_data)
                except:
                    pass
            else:
                print "[%s, %s] : disconnect" % client_address
                client_socket.close()
                carCtrl.stop()
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

    carCtrl = carCtrl.CarCtrl(13, 12, 15, 16, 0, 7, 32)
    servoCtrl = servoCtrl.ServoCtrl(1, 2)
    robotArmCtrl = robotArmCtrl.RobotArmCtrl(3, 4, 5, 6)
    jsonCtrl = jsonAnalysis.JsonAnalysis(servoCtrl, carCtrl, robotArmCtrl)

    print "******Server Online*****"
    print "***", host, port, "***"
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print "*" * 30
            print "[%s, %s] : connected" % client_address
            handle_client(client_socket, client_address)

    except KeyboardInterrupt:
        print "******Server Offline*****"
        robotArmCtrl.clean()
        # client_socket.close()
        server_socket.close()
