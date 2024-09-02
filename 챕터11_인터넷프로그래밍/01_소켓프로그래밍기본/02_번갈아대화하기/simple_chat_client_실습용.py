import socket
import pickle

SERVER_IP = "192.168.1.10"  # 접속할 서버의 IP 주소를 명확히 지정
SERVER_PORT = 7470  # # 접속할 서버의 포트를 명확히 지정

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((SERVER_IP, SERVER_PORT))  # 서버에 연결 (Blocking)

    print("서버에에 연결되었습니다.")

    pass

    print("연결이 종료되었습니다.")
