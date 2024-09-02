# CPU-Bound 예시 (Numpy 사용)

import numpy as np

import time


class Timer:
    def __init__(self):
        self.start = time.time()

    def __enter__(self):
        return self  # as로 사용할 수 있도록 self 반환

    def __exit__(self, *args):
        print("Elapsed time = ", time.time() - self.start)


def process_work(data):
    for r in range(5):
        data = np.sqrt(data)
        data = np.exp(data)
        data = np.power(data, 0.1)
    return data.sum()


if __name__ == "__main__":

    np.random.seed(0)

    # 데이터 만드는 시간은 제외
    data = np.random.rand(100_000_000)

    with Timer():

        result = process_work(data)

    print(result)

"""
Elapsed time =  15.031172752380371
111116795.31966303
"""
