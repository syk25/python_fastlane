""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

from tkinter import *

from PIL import Image, ImageDraw
import numpy as np
import torch

# 네트워크 정의는 훈련 코드에서 복사해와야 함
model = torch.nn.Sequential(
    # 여기에 작성
)

model.load_state_dict(torch.load("my_mnist_trained.pth"))


class MyPaint(Tk):
    def __init__(self):
        super().__init__()

        self.title("My Paint")

        # 가장 최근의 마우스 좌표
        self.old_x = None
        self.old_y = None

        self.canvas = Canvas(self, width=600, height=600, bg="black")
        self.canvas.bind("<Button-1>", self.draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_xy)

        self.label = Label(self, text="", font=("Arial", 25))
        self.button = Button(
            self, text="Reset", font=("Arial", 25), command=self.reset_display
        )

        self.canvas.pack(fill=BOTH, expand=True)
        self.label.pack(fill=BOTH, expand=True)
        self.button.pack(fill=BOTH, expand=True)

        self.image = Image.new("RGB", (600, 600), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

    def reset_display(self):
        self.canvas.delete("all")
        self.draw.rectangle((0, 0, 600, 600), fill=(0, 0, 0, 0))
        self.label["text"] = ""

    def draw(self, e):
        if self.old_x and self.old_y:
            self.canvas.create_line(
                self.old_x, self.old_y, e.x, e.y, width=3, fill="white", smooth=True
            )
            self.draw.line(
                [self.old_x, self.old_y, e.x, e.y], fill=(255, 255, 255), width=3
            )

        self.old_x = e.x
        self.old_y = e.y

    def reset_xy(self, e):
        self.old_x = None
        self.old_y = None

        img = self.image.resize((28, 28))
        img = np.array(img)
        img = np.where(img > 0, 255, 0)  # 이미지 진하게 만들기

        # Image.fromarray(img.astype(np.uint8)).save("my_drawing.png")  # 디버깅용

        img = img[:, :, 0]

        x_input = np.expand_dims(img, axis=0) / 255.0
        x_input = torch.from_numpy(x_input.astype(np.float32)).flatten(start_dim=1)
        y_pre = model(x_input)
        self.label["text"] = str(y_pre.argmax(axis=1)[0])


if __name__ == "__main__":
    MyPaint().mainloop()
