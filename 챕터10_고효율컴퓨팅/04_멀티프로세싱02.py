"""
주피터 노트북에서는 멀티프로세싱이 정상적으로 작동하지 않습니다.
"""

# 멀티프로세싱은 메모리를 별도로 사용합니다.

import multiprocessing
import os


def process_work(message):
    global g
    print(message, id(g))  # 전역인데 주소가??
    g += 1
    print(multiprocessing.current_process(), g)  # 분명히 1이 더해졌는데


g = 0

if __name__ == "__main__":

    p1 = multiprocessing.Process(target=process_work, args=("First thread",))
    p2 = multiprocessing.Process(target=process_work, args=("Second thread",))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(g)  # 여기서는 그대로 0
