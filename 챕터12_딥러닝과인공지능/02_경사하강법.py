""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

"""
경사하강법
Gradient descent
"""

import torch
import numpy as np


# x = 1.0에서 시작
x = torch.tensor([1.0], requires_grad=True)

learning_rate = 1e-3


def my_func(x):
    return x**2  # y = x*x


def gradient_descent():
    global x

    y = my_func(x)

    x.grad = None  # gradient가 누적되는 것을 방지
    y.backward()

    with torch.no_grad():  # gradient 계산과는 무관하다
        x -= learning_rate * x.grad


# 가시화 애니메이션
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(14, 8))

axis = plt.axes(xlim=(-1.4, 1.4), ylim=(-0.2, 1.6))

(line,) = plt.plot(np.linspace(-1.2, 1.2, 100), my_func(np.linspace(-1.2, 1.2, 100)))
scatter = axis.scatter(x.detach().numpy(), my_func(x).detach().numpy(), c="red")


def init():
    scatter.set_offsets(torch.cat([x, my_func(x)], dim=0).detach().numpy())
    return (line, scatter)


def animate(i):
    gradient_descent()
    scatter.set_offsets(torch.cat([x, my_func(x)], dim=0).detach().numpy())
    return (line, scatter)


anim = FuncAnimation(fig, animate, init_func=init, frames=200, interval=1, blit=True)

plt.show()
