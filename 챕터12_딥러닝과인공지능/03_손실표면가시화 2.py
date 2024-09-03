""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

import random
import numpy as np


class LinearModel:
    def __init__(self):
        self.a = random.random()
        self.b = random.random()

    def __call__(self, x):
        y = self.a * x + self.b
        return y


model = LinearModel()

x_input = np.array([1, 5, 8])
y_target = np.array([15, 55, 60])

learning_rate = 1e-4

loss_history = []
a_history = []
b_history = []

for i in range(1000):

    grad_a = 0.0
    grad_b = 0.0
    loss_sum = 0.0

    y_pred = model(x_input)

    error = y_pred - y_target
    loss = (error**2).mean()

    grad_a = (error * x_input).mean()
    grad_b = error.mean()

    model.a -= learning_rate * grad_a
    model.b -= learning_rate * grad_b

    loss_history.append(loss.sum())
    a_history.append(model.a)
    b_history.append(model.b)

    if i % 60 == 0:
        print("Loss = ", loss.sum())


# Loss surface
import matplotlib.pyplot as plt

x = np.array([1, 5, 8])
y_target = np.array([15, 55, 60])

la = max(a_history) - min(a_history)
lb = max(b_history) - min(b_history)

a = np.arange(min(a_history) - 0.1 * la, max(a_history) + 0.1 * la, 0.1)
b = np.arange(min(b_history) - 0.1 * lb, max(b_history) + 0.1 * lb, 0.1)
A, B = np.meshgrid(a, b)

Z = sum([(A * x[i] + B - y_target[i]) ** 2 / x.shape[0] for i in range(x.shape[0])])

from matplotlib import cm

# https://matplotlib.org/stable/gallery/mplot3d/surface3d.html
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(
    A, B, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False, alpha=0.5
)
ax.scatter3D(
    a_history[::50],
    b_history[::50],
    np.array(loss_history[::50]) + 10.0,
    c="blue",
    alpha=1.0,
)
ax.set_xlabel("a")
ax.set_ylabel("b")
ax.set_zlabel("Loss")
plt.show()
