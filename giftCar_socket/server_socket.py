# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/31 15:05

import socket
import json
import car_pwm_ctrl

host = "192.168.100.2"
port = 8989


def handle_client(client_socket, client_address):
    while True:
        try:
            request_data = client_socket.recv(1024)
            if request_data:
                print "request_data:", request_data
                try:
                    json_data = json.loads(request_data)
                    if json_data.get("UD") is not None:
                        car_pwm_ctrl.left_wheel(int(json_data.get("UD")))
                        car_pwm_ctrl.right_wheel(int(json_data.get("UD")))
                    if json_data.get("LR") is not None:
                        car_pwm_ctrl.dir_ctrl(int(json_data.get("LR")))
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

    car_pwm_ctrl = car_pwm_ctrl.Car_pwm_ctrl(29, 12, 15, 16, 0)
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
