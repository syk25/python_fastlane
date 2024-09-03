""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

from tkinter import *
from PIL import Image, ImageTk
import torch
import hlab_fast_neural_style


def cartoonify(img, pretrained, size):
    model = torch.hub.load(
        "bryandlee/animegan2-pytorch:main", "generator", pretrained=pretrained
    )
    face2paint = torch.hub.load(
        "bryandlee/animegan2-pytorch:main", "face2paint", size=size
    )
    return face2paint(model, img)


def read_square_image(filename, size):
    """이미지를 읽어서 가운데를 1:1 aspect ratio로 잘라내고 크기 변경"""

    img = Image.open(filename).convert("RGB")

    w, h = img.size
    if w > h:
        d = (w - h) // 2
        img = img.crop((d, 0, h + d, h))
    else:
        d = (h - w) // 2
        img = img.crop((0, d, w, w + d))

    return img.resize((size, size), Image.ANTIALIAS)


# 주의: ImageTk 생성은 window = Tk() 이후에 호출
def tk_images(img):
    preview = img.resize((PREVIEW_SIZE, PREVIEW_SIZE), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img), ImageTk.PhotoImage(preview)


def normal_click():
    display.create_image(0, 0, anchor=NW, image=normal_tk)


def paprika_click():
    pass


def mosaic_click():
    pass


def candy_click():
    pass


DISPLAY_SIZE = 640
PREVIEW_SIZE = 154

window = Tk()

img = read_square_image("jmhong_face.jpg", DISPLAY_SIZE)
normal_tk, normal_preview = tk_images(img)


display = Canvas(window, width=DISPLAY_SIZE, height=DISPLAY_SIZE, bg="white")
display.create_image(0, 0, anchor=NW, image=normal_tk)


frame_previews = Frame(window)

frame_normal = Frame(frame_previews)

label_normal = Label(frame_normal, text="Normal", bg="white")

button_normal = Button(
    frame_normal, text="Normal", command=normal_click, image=normal_preview
)


label_normal.pack(side=TOP, fill=BOTH, expand=False)
button_normal.pack(side=TOP, fill=BOTH, expand=False)


frame_normal.pack(side=LEFT, fill=BOTH, expand=False)

display.pack(side=TOP, fill=BOTH, expand=True)
frame_previews.pack(side=TOP, fill=BOTH, expand=True)

window.mainloop()
