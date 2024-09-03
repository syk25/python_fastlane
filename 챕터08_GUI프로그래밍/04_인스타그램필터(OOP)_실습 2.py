""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

from tkinter import *
from PIL import Image, ImageTk
import torch

from PIL import Image
import hlab_fast_neural_style

DISPLAY_SIZE = 640
PREVIEW_SIZE = 154


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


def cartoonify(img, pretrained, size):
    model = torch.hub.load(
        "bryandlee/animegan2-pytorch:main", "generator", pretrained=pretrained
    )
    face2paint = torch.hub.load(
        "bryandlee/animegan2-pytorch:main", "face2paint", size=size
    )
    return face2paint(model, img)


def tk_images(img):
    preview = img.resize((PREVIEW_SIZE, PREVIEW_SIZE), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img), ImageTk.PhotoImage(preview)


class PreviewFrame(Frame):
    def __init__(self, master, img, name):
        pass

    def update_display(self):
        global display
        pass


img = read_square_image("jmhong_face.jpg", DISPLAY_SIZE)


window = Tk()


previews_frame = Frame(window)

normal = PreviewFrame(previews_frame, img, "Normal")
paprika = PreviewFrame(
    previews_frame, cartoonify(img, "paprika", DISPLAY_SIZE), "Paprika"
)
mosaic = PreviewFrame(
    previews_frame,
    hlab_fast_neural_style.stylize(img, "saved_models/mosaic.pth"),
    "Mosaic",
)
candy = PreviewFrame(
    previews_frame,
    hlab_fast_neural_style.stylize(img, "saved_models/candy.pth"),
    "Candy",
)

display = Label(window, image=normal.img)
# display가 Label이면 display["image"] = normal.img 와 같이 이미지 변경 가능
# 캔버스 사용할 경우
# display = Canvas(window, width=DISPLAY_SIZE, height=DISPLAY_SIZE, bg="white")
# display.create_image(0, 0, anchor=NW, image=normal.img)

normal.pack(side=LEFT, fill=BOTH, expand=False)
paprika.pack(side=LEFT, fill=BOTH, expand=False)
mosaic.pack(side=LEFT, fill=BOTH, expand=False)
candy.pack(side=LEFT, fill=BOTH, expand=False)

display.pack(side=TOP, fill=BOTH, expand=True)
previews_frame.pack(side=TOP, fill=BOTH, expand=True)

window.mainloop()
