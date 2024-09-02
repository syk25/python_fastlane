""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

import socket
import pickle
import threading

IP_ADDR = socket.gethostbyname(socket.gethostname())
PORT = 7470

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind((IP_ADDR, PORT))
my_socket.listen()
print(f"Started server at {my_socket.getsockname()}")

client_list = []


def forward(data):
    for c in client_list.copy():
        try:
            c.sendall(data)
        except:
            client_list.remove(c)


def handler(conn):
    global client_list
    while conn in client_list:
        try:
            data = conn.recv(1024)
            print("받은 데이터: ", pickle.loads(data))
        except:
            break  # 클라이언트 연결 오류

        forward(data)


while True:
    conn, addr = my_socket.accept()  # 연결을 받아들임 (Blocking)
    client_list.append(conn)

    print(f"Connection from {addr}")

    new_thread = threading.Thread(target=handler, args=(conn,))
    new_thread.start()

my_socket.close()
