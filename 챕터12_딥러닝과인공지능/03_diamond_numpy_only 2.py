""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

# 데이터셋 읽어들이기
import pandas as pd

df = pd.read_csv("diamonds.csv")

df.plot.scatter(x="carat", y="price", s=0.1, figsize=(9, 4))


# 선형 회귀
import random
import numpy as np
import copy


class LinearModel:
    def __init__(self):
        self.a = random.random()
        self.b = random.random()

        # torch.manual_seed(0)에서 복사해온 데이터
        self.a, self.b = 1.5409960746765137, -0.293428897857666

    def __call__(self, x):
        y = self.a * x + self.b
        return y


model = LinearModel()

x_input = df["carat"].to_numpy()
y_target = df["price"].to_numpy()

learning_rate = 1e-1

num_epochs = 400

loss_history = []
model_history = []

for epoch in range(1, num_epochs + 1):

    y_pred = model(x_input)

    error = y_pred - y_target
    loss = (error**2).mean()  # Mean Squared Error Loss

    grad_a = 2.0 * (error * x_input).mean()
    grad_b = 2.0 * error.mean()

    model.a -= learning_rate * grad_a
    model.b -= learning_rate * grad_b

    loss_history.append(loss)
    model_history.append(copy.deepcopy(model))

    if epoch % (num_epochs // 10) == 0:
        print(f"Epoch {epoch}: loss = {loss.item()}")

# 그래프로 결과 확인
import matplotlib.pyplot as plt
import math


def visualize(x_input, y_target, loss_history, model_history):

    plt.figure(figsize=(24, 6))

    plt.subplot(141)

    plt.scatter(x_input, y_target, s=100)  # 모든 데이터 샘플 그리기

    # 훈련 마지막 모델의 출력 그리기
    x = np.linspace(x_input.min(), x_input.max(), 10)
    y = model_history[-1](x)
    plt.plot(x, y, c="red")
    # [참고] tensor.detach().numpy(): 훈련에 필요한 정보들은 빼고 순수 값만 넘파이로 변환

    plt.subplot(142)

    num_steps = len(loss_history) // 10
    plt.scatter(x_input, y_target, s=100)  # 샘플 그리기
    colors = plt.cm.rainbow(np.linspace(0, 1, 10))
    for i in range(0, len(model_history), num_steps):
        y = model_history[i](x)
        plt.plot(x, y, c=colors[i // num_steps])

    plt.subplot(143)

    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.plot(loss_history)

    plt.subplot(144)

    plt.xlabel("Epoch")
    plt.ylabel("Log loss")
    plt.plot([math.log(l) for l in loss_history])

    plt.show()


visualize(x_input, y_target, loss_history, model_history)
