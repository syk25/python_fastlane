"""
주피터 노트북에서는 멀티프로세싱이 정상적으로 작동하지 않습니다.
"""

# 멀티프로세싱의 기본적인 사용 방법

import multiprocessing
import os


def process_work(message):
    print("Process ID", os.getpid())  # 프로세스 아이디
    print(multiprocessing.current_process())
    print(message)


if __name__ == "__main__":

    print("# of cpus", multiprocessing.cpu_count())
    print("Parent Process ID", os.getpid())  # 프로세스 아이디

    p1 = multiprocessing.Process(target=process_work, args=("First thread",))
    p2 = multiprocessing.Process(target=process_work, args=("Second thread",))

    p1.start()
    p2.start()

    print("P1 pid", p1.pid)
    print("P2 pid", p2.pid)

    p1.join()
    p2.join()
