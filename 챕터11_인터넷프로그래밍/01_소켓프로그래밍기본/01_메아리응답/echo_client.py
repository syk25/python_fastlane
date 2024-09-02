import socket
import pickle  # 데이터 직렬화 사용

SERVER_IP = "192.168.1.10"  # 접속할 서버의 IP 주소를 명확히 지정
SERVER_PORT = 7470  # # 접속할 서버의 포트를 명확히 지정

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((SERVER_IP, SERVER_PORT))  # 서버에 연결 (Blocking)

    s.sendall(pickle.dumps("Hello, internet!"))  # 소켓을 통해서 데이터 보내기

    data = s.recv(1024)  # 소켓을 통해서 최대 1024 바이트까지 데이터를 받아들임

    print(f"돌려받은 데이터: {pickle.loads(data)}")
