# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/31 15:05

import json
import socket
import select
import threading
from carCtrl import robotArmCtrl, jsonAnalysis, carCtrl, servoCtrl, updateCtrl

host = "0.0.0.0"
port = 8989

connected = False


def handle_client(client_socket, client_address):
    """处理客户端"""
    global connected
    connected = True
    client_socket.send("OK\r\n".encode("utf-8"))
    client_socket.settimeout(8)
    carCtrl.set_client_socket(client_socket)  # 当连接上客户端，设置socket，以便速度和避障上传
    update_ctrl = updateCtrl.UpdateCtrl(client_socket, dht11_pin)
    timer = threading.Timer(0.2, send_data, args=["all", update_ctrl])
    timer.start()
    while True:
        try:
            request_data = client_socket.recv(1024)
            if request_data:
                try:
                    print("request_data:", request_data)
                    json_datas = request_data.split("*")
                    print("json_ datas:", json_datas)
                    for json_data in json_datas:
                        if json_data != '':
                            json_data_now = json.loads(json_data)
                            jsonCtrl.analysis(json_data_now)
                except:
                    print("json error")
            else:
                print("[%s, %s] : disconnect" % client_address)
                connected = False
                carCtrl.set_client_socket(None)
                client_socket.close()
                carCtrl.stop()
                return

        except Exception as e:
            print(e)
            print("[%s, %s] : disconnect" % client_address)
            carCtrl.set_client_socket(None)
            connected = False
            carCtrl.stop()
            client_socket.close()
            return


def send_data(key, update_ctrl):
    """ 上传数据"""
    if connected is True:
        if key == "dht":
            update_ctrl.updateDHT11()
            timer = threading.Timer(2, send_data, args=["dht", update_ctrl])
            timer.start()
        elif key == "mpu":
            update_ctrl.updateMpu9250()
            timer = threading.Timer(0.1, send_data, args=["mpu", update_ctrl])
            timer.start()
        elif key == "all":
            update_ctrl.updateDHT11()
            timer = threading.Timer(2, send_data, args=["dht", update_ctrl])
            timer.start()
            update_ctrl.updateMpu9250()
            timer = threading.Timer(0.1, send_data, args=["mpu", update_ctrl])
            timer.start()
    else:
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
    dht11_pin = 20  # 20为BCM, Physical:38
    print("******Server Online*****")
    print("***", host, port, "***")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print("*" * 30)
            print("[%s, %s] : connected" % client_address)
            handle_client(client_socket, client_address)

    except KeyboardInterrupt:
        print("******Server Offline*****")
        robotArmCtrl.clean()
        # client_socket.close()
        server_socket.close()
