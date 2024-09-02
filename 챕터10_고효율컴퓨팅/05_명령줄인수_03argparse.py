"""
argparse로 더 안전하게 사용하기
https://docs.python.org/3/library/argparse.html

[참고] Parse: 문장을 분석
"""

import argparse


def multiple_print(word: str, num: int):
    for _ in range(num):
        print(word)


def init_argparse():
    parser = argparse.ArgumentParser(description="문자열을 여러 번 출력")  # description 생략 가능
    parser.add_argument("-w", "--word", help="String to print", type=str, default="헬로!")
    parser.add_argument("-n", "--num", help="Number of repeating", type=int, default=1)
    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()

    print(args.word, type(args.word))
    print(args.num, type(args.num))

    multiple_print(args.word, args.num)
