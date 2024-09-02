""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

from tkinter import *
from tkinter import simpledialog
import socket
import pickle
import threading

SERVER_IP = "YOUR_IP_HERE"  # 접속할 서버의 IP 주소를 명확히 지정
SERVER_PORT = 7470  # # 접속할 서버의 포트를 명확히 지정


class ClientGUI(Tk):
    def __init__(self):
        super().__init__()
        self.input_user_name()
        self.title(f"{self.user_name} 메신저")  # 윈도우 이름

        self.text_box = Text(
            master=self,
            width=50,
            height=10,
            fg="black",
            bg="#B2C7D9",
        )

        self.entry = Entry(
            master=self,
            fg="black",
            bg="white",
            width=50,
            justify=LEFT,
        )

        self.entry.bind("<Return>", lambda _: self.send_message())
        self.text_box.pack()
        self.entry.pack()

        # 소켓 초기화 작업
        pass

        # 항상 메시지를 받을 준비가 되어 있는 쓰레드 실행
        pass

        # 입장 메시지 서버로 전송
        pass

    def input_user_name(self):
        self.withdraw()  # 아래의 다이얼로그가 먼저 보이게 하기 위해서 임시로 윈도우 감추기
        self.user_name = simpledialog.askstring(
            "대화명 입력창",
            "대화명을 입력해주세요.",
            parent=self,
        )
        self.deiconify()  # 대화명 입력 후 다시 윈도우 보이게 하기

    def insert_text(self, t):
        print("서버:", t)
        self.text_box.configure(state="normal")  # 텍스트 변경 허용
        self.text_box.insert(index=END, chars=t + "\n")
        self.text_box.see(END)  # 가장 마지막에 추가된 메시지가 보이도록
        self.text_box.configure(state="disabled")  # 텍스트에 직접 입력 금지

    def send_message(self):
        msg_to_send = f"{self.user_name}: {self.entry.get()}"

        # 메시지 전송
        pass

        self.entry.delete(0, END)  # 엔터 입력시 입력창 지우기

    def recv_message(self):
        while True:
            # 서버로부터 메시지 받기
            # 받은 메시지를 insert_text로 대화창에 표시
            pass

    def run(self):
        self.mainloop()

        # 퇴장 메시지 전송
        # 소켓 닫기
        pass


if __name__ == "__main__":
    ClientGUI().run()
