# https://docs.python.org/3/library/turtle.html

import turtle

t = turtle.Turtle()

# turtle.setup(1280, 960)
# turtle.screensize(400, 300)
t.speed("slow")
t.shape("turtle")
t.turtlesize(2)
t.color("green")
t.pencolor("blue")
t.screen.bgcolor("aqua")

"""함수로 코드 모듈화"""


def draw_square():
    for i in range(4):
        t.forward(200)
        t.left(90)


def draw_triangle():
    for i in range(3):
        t.forward(200)
        t.left(120)


def draw_hexagon():
    for i in range(6):
        t.forward(200)
        t.left(60)


""" 문제: 정사각형 그리기 """
# 풀이1: 일일이 쓰기 -> 처음에는 일일이 쓴다. 패턴을 발견하면 반복문으로 교체
# t.forward(200)
# t.left(90)
# t.forward(200)
# t.left(90)
# t.forward(200)
# t.left(90)
# t.forward(200)
# t.left(90)

# 풀이2: 풀이1을 보고 규칙성을 발견 후에 반복문으로 변환
# for i in range(4):
#     t.forward(200)
#     t.left(90)

"""문제: 정사각형 4개 그리기"""
# 풀이
# for j in range(4):
#     draw_square()
#     t.left(90)

""" 문제3: 다이아몬드 형태의 정사각형 8개 그리기 """
# 풀이
# for j in range(6):
#     draw_triangle()
#     t.left(60)

""" 문제4: 육각형을 꽃처럼 그리기"""
# 풀이
for j in range(12):
    draw_hexagon()
    t.left(30)


turtle.done()
