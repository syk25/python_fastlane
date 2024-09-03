""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

# 데이터 읽어들이기
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from PIL import Image
import matplotlib.pyplot as plt

# MNIST database http://yann.lecun.com/exdb/mnist/
# Modified National Institute of Standards
# 여기서는 데이터 양이 많지 않기 때문에 한 번에 읽어온다.
# 여러가지로 바꿔보면서 정밀도 높여보기
# 훈련에 몇 분 정도는 걸립니다.

# images는 (60000, 28, 28), np.float64, 0.0~1.0 (1.0은 흰색, 0.0은 검은색)
# Label은 (60000,), np.uint8

x_train = np.load("MNIST_x_train.npy")
x_test = np.load("MNIST_x_test.npy")
y_train = np.load("MNIST_y_train.npy")
y_test = np.load("MNIST_y_test.npy")

# print(x_train.shape, x_train.dtype)  # (60000, 28, 28) float64
# print(y_train.shape, y_train.dtype)  # (60000,) uint8

# Pillow로 이미지 확인
# print(y_train[123])  # 7
# img = Image.fromarray(np.uint8(x_train[123] * 255.0)).convert("RGB")
# img.show()

# Matplot으로 이미지 확인
# print(y_train[123])  # 7
# plt.imshow(x_train[123], cmap="gray")
# plt.show()
# exit(-1)
