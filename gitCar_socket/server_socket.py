# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/31 15:05

import socket
import json
host = "192.168.100.3"
port = 8989


def handle_client(client_socket):
    request_data = client_socket.recv(1024)
    if request_data:
        print "request_data:", request_data
        try:
            json_data = json.loads(request_data)



if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.bind((host, port))
    server_socket.listen(3)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print "*" * 30
            print "[%s, %s] : connected" % client_address
            handle_client(client_socket)
    except KeyboardInterrupt:
        print "******Smart Farm Server Offline*****"
        server_socket.close()
