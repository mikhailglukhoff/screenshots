import os.path
import socket
import time

from settings import server_host_port


def send_file(file_path):
    host, port = server_host_port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        with open(file_path, 'rb') as file:
            file_name = os.path.basename(file_path)
            print('FILE NAME: ', file_name)
            client_socket.sendall(file_name.encode())

            time.sleep(0.1)

            client_socket.sendall(file.read())
