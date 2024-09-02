# CPU-Bound 예시

import multiprocessing
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
    # print(multiprocessing.current_process())
    for r in range(100):
        data = np.sqrt(data)
        data = np.exp(data)
        data = np.power(data, 0.1)
    return data.sum()


if __name__ == "__main__":

    np.random.seed(0)

    # 데이터 만드는 시간은 제외
    data = np.random.rand(100_000_000)

    with Timer():

        # 프로세스 별로 데이터 나누기
        # [힌트] Numpy split
        result = process_work(data)  # 멀티프로세싱 없이 Numpy만 사용할 경우

    print(result)


""" 
AMD Ryzen 9 3900X 기준

멀티 프로세싱 없이 Numpy 사용
Elapsed time =  15.031172752380371
111116795.31966303

4
Elapsed time =  5.668000936508179
111116795.3196635

10
Elapsed time =  3.1419990062713623
111116795.31966339

20
Elapsed time =  2.5809988975524902
111116795.31966342

40
Elapsed time =  2.2569985389709473
111116795.3196634

100
Elapsed time =  2.3669955730438232
111116795.31966344

200
Elapsed time =  2.396998882293701
111116795.31966335
"""
