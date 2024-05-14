# import os
# import socket
# from dotenv import load_dotenv
# import time
# import logging
#
# import settings
#
# load_dotenv()
#
# server_file_path = os.getenv("SERVER_FILE_PATH")
# server_host = os.getenv("SERVER_HOST")
# server_port = int(os.getenv("SERVER_PORT"))
#
# file_path = os.getenv("SCREENSHOTS_DIRECTORY")
#
# logging.basicConfig(filename=f'{settings.log_dir}/error.log',
#                     level=logging.ERROR,
#                     format='%(asctime)s - %(levelname)s - %(message)s')
#
#
# def send_file(file_path):
#     host, port = server_host, server_port
#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#             client_socket.connect((host, port))
#
#             with open(file_path, 'rb') as file:
#                 file_name = os.path.basename(file_path)
#                 print('FILE NAME: ', file_name)
#                 client_socket.sendall(file_name.encode())
#
#                 time.sleep(0.1)
#
#                 client_socket.sendall(file.read())
#         return True
#
#     except ConnectionRefusedError as e:
#         logging.error(f"ConnectionRefusedError: {e}")
#     except TimeoutError as e:
#         logging.error(f"TimeoutError: {e}")
#     except FileNotFoundError as e:
#         logging.error(f"FileNotFoundError: {e}")
