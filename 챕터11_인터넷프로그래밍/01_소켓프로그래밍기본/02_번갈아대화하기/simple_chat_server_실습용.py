import socket
import pickle

IP_ADDR = socket.gethostbyname(socket.gethostname())
PORT = 7470

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((IP_ADDR, PORT))
    s.listen()

    conn, addr = s.accept()

    with conn:
        conn.sendall(pickle.dumps("환영합니다."))

        pass

        print(f"{addr}와 연결이 종료되었습니다.")
