"""
코드가 길거나 작업량이 많은 경우에는 주피터 노트북 보다는 스크립트 모드를 사용합니다.
옵션을 조금씩 바꿔가면서 실험을 반복할 경우에는 코드 수정이 번거롭습니다.
이럴 때 명령줄 인수를 사용하면 더 편리하고 안정적입니다.
"""

import sys

if __name__ == "__main__":

    print(type(sys.argv))  # argument vector
    print("Num of arguments:", len(sys.argv))

    for i, arg in enumerate(sys.argv):
        print(i, arg, type(arg))
