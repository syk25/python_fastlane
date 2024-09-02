""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""
import socket
import pickle
import cv2
import time

# 동영상 파일 경로 주의하세요
# 캠을 사용하면 라이브 방송!
cap = cv2.VideoCapture("Ch11_인터넷프로그래밍/04_비디오스트리밍/jmhong_face.mp4")

IP_ADDR = socket.gethostbyname(socket.gethostname())
PORT = 7470

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind((IP_ADDR, PORT))
my_socket.listen()
print(f"Started server at {my_socket.getsockname()}")

conn, addr = my_socket.accept()
print(f"Connection from {addr}")

previous_time = time.perf_counter()

while True:
    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 무한 반복
        continue

    frame = cv2.resize(frame, (320 * 2, 180 * 2))

    # 인코딩으로 용량 줄이기 (옵션)
    ret, frame = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

    data = pickle.dumps(frame)
    conn.sendall(len(data).to_bytes(8, "little"))  # 데이터 사이즈를 먼저 전송
    conn.recv(8)  # OK echo from client
    conn.sendall(data)

    # cv2.imshow("Server", frame)

    # 30fps와 비슷해지도록 대기 시간 조절
    new_time = time.perf_counter()
    time_to_wait = max(33 - int((new_time - previous_time) * 1000.0), 1)
    if cv2.waitKey(time_to_wait) == ord("q"):
        break
    previous_time = new_time

cv2.destroyAllWindows()
cap.release()
my_socket.close()

"""
연습문제
- 여러 클라이언트들이 아무 때나 접속해서 중간부터 동영상을 볼 수 있도록 기능 확장
"""
