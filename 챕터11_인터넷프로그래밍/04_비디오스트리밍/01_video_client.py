""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

import socket
import pickle
import cv2

SERVER_IP = "192.168.1.10"
SERVER_PORT = 7470
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:

    my_socket.connect((SERVER_IP, SERVER_PORT))

    while True:

        size_to_receive = int.from_bytes(my_socket.recv(8), byteorder="little")
        my_socket.sendall(
            size_to_receive.to_bytes(8, byteorder="little")
        )  # Echo to server

        # 버퍼 사이즈보다 큰 데이터 받기
        data = []
        while size_to_receive > 0:
            packet = my_socket.recv(min(BUFFER_SIZE, size_to_receive))
            data.append(packet)
            size_to_receive -= len(packet)

        frame = pickle.loads(bytes().join(data))

        # 서버에서 인코딩했을 경우 디코딩 (옵션)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        cv2.imshow("Client", frame)

        if cv2.waitKey(1) == ord("q"):
            break

cv2.destroyAllWindows()
