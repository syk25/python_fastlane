"""
스크립트를 함수처럼 사용하기
"""

import sys


def multiple_print(word: str, num: int):
    for _ in range(num):
        print(word)


if __name__ == "__main__":
    # 세 번째 인수를 정수로 변환
    multiple_print(sys.argv[1], int(sys.argv[2]))
