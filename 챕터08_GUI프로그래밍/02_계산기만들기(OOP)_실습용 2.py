""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""


""" OOP 구조로 바꿔보세요. """

# OOP style

from tkinter import *


class MyCalculator(Tk):

    BUTTON_TEXTS = [
        ["C", "/", "//", "-"],
        ["7", "8", "9", "+"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "%"],
        ["0", "**", ".", "="],
    ]

    def __init__(self):
        pass

    def button_click(self, key):
        pass


def main():
    MyCalculator().mainloop()


if __name__ == "__main__":
    main()
