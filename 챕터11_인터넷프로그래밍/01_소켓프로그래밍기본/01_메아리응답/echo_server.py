import socket
import pickle  # 데이터 직렬화 사용

# IP_ADDR = "127.0.0.1" # 같은 컴퓨터에서 접속해올 때
# IP_ADDR = "192.168.1.10"
IP_ADDR = socket.gethostbyname(socket.gethostname())

# https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
# PORT = 0  # 운영체제가 비어있는 포트에 배정
PORT = 7470

# AF_INET: IPv4
# AF_INET6: IPv6
# SOCK_STREAM: TCP (Transmission Control Protocol)
# SOCK_DGRAM: UDP (User Datagram Protocol)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((IP_ADDR, PORT))  # 소켓에 IP 주소 연결
    s.listen()  # 다른 컴퓨터로부터 연결을 받을 수 있도록 설정

    print(f"Started server at {s.getsockname()}")

    conn, addr = s.accept()  # 연결을 받아들임 (Blocking)
    with conn:
        print(f"Connection from {addr}")

        data = conn.recv(1024)  # 소켓을 통해서 최대 1024 바이트까지 데이터를 받아들임
        # print(type(data))  # <class 'bytes'>

        print("받은 데이터: ", pickle.loads(data))

        conn.sendall(data)  # 받은 데이터를 그대로 돌려보냄

        print(f"Close connection from {addr}")
