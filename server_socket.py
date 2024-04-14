import os
import socket

from settings import server_file_path, server_host_port


def receive_file():
    host, port = server_host_port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)

        print("Waiting for connection...")

        while True:
            connection, address = server_socket.accept()
            print("Connected by", address)

            file_name = connection.recv(1024).decode()

            file_path = os.path.join(server_file_path, file_name)

            with open(file_path, 'wb') as file:
                while True:
                    data = connection.recv(4096)
                    if not data:
                        break
                    file.write(data)

            print(f"File {file_name} received successfully.")


            connection.close()


if __name__ == "__main__":
    receive_file()
