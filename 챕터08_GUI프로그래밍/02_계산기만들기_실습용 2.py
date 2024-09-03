""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

""" 계산기 만들기
힌트
- 시작할때 0, C를 눌러도 0, 숫자를 입력하면 0을 삭제 후 숫자로.
- '='를 누르면 계산 결과 출력(eval() 사용)
- 계산할 수 없는 입력이면 ERROR 출력
- ERROR 일 때 다시 키를 누르면 재시작 
- 람다가 캡쳐하는거 설명
"""

import tkinter as tk

window = tk.Tk()

window.title("My Calculator")

button_texts = [
    ["C", "/", "//", "-"],
    ["7", "8", "9", "+"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "%"],
    ["0", "**", ".", "="],
]
