"""
주피터 노트북에서는 멀티프로세싱이 정상적으로 작동하지 않습니다.
"""

# 프로세스 풀(Pool)과 동기화(Synchronization)

import multiprocessing
import os


def process_work(i):
    return i * i  # 반환!


if __name__ == "__main__":

    my_list = [1, 2, 3, 4, 5]

    p = multiprocessing.Pool()

    result = p.map(process_work, my_list)

    print(result)
