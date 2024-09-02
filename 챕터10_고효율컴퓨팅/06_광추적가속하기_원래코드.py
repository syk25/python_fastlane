"""
"Ray Tracing From Scratch in Python" by Omar Aflak
글 링크: https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
코드 링크: https://gist.github.com/OmarAflak/08eed161f5390c27fc8fed136f2ff53d#file-medium_ray_tracing_code_13-py

[실습 문제]
1. 멀티프로세싱으로 더 빠르게 만들기
2. width, height, max_depth, num_split(몇 개로 나눌지)등을 argparse로 입력받기
3. num_split vs elapsed_time 그래프 그려보기

* 이 예제에서는 OOP 적용 같은 코드 정리에는 신경을 쓰지 않겠습니다.
"""

import numpy as np
import matplotlib.pyplot as plt
import time


class Timer:
    def __init__(self):
        self.start = time.perf_counter()

    def __enter__(self):
        return self  # as로 사용할 수 있도록 self 반환

    def __exit__(self, *args):
        print("Elapsed time = ", time.perf_counter() - self.start)


def normalize(vector):
    return vector / np.linalg.norm(vector)


def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis


def sphere_intersect(center, radius, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None


def nearest_intersected_object(objects, ray_origin, ray_direction):
    distances = [
        sphere_intersect(obj["center"], obj["radius"], ray_origin, ray_direction)
        for obj in objects
    ]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance


# 이미지 해상도
width = 400
height = 300

# 빛의 반사를 몇 회까지 추적할 것인지 결정 (정밀도)
max_depth = 3

camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1 / ratio, 1, -1 / ratio)  # left, top, right, bottom

light = {
    "position": np.array([5, 5, 5]),
    "ambient": np.array([1, 1, 1]),
    "diffuse": np.array([1, 1, 1]),
    "specular": np.array([1, 1, 1]),
}

objects = [
    {
        "center": np.array([-0.2, 0, -1]),
        "radius": 0.7,
        "ambient": np.array([0.1, 0, 0]),
        "diffuse": np.array([0.7, 0, 0]),
        "specular": np.array([1, 1, 1]),
        "shininess": 100,
        "reflection": 0.5,
    },
    {
        "center": np.array([0.1, -0.3, 0]),
        "radius": 0.1,
        "ambient": np.array([0.1, 0, 0.1]),
        "diffuse": np.array([0.7, 0, 0.7]),
        "specular": np.array([1, 1, 1]),
        "shininess": 100,
        "reflection": 0.5,
    },
    {
        "center": np.array([-0.3, 0, 0]),
        "radius": 0.15,
        "ambient": np.array([0, 0.1, 0]),
        "diffuse": np.array([0, 0.6, 0]),
        "specular": np.array([1, 1, 1]),
        "shininess": 100,
        "reflection": 0.5,
    },
    {
        "center": np.array([0, -9000, 0]),
        "radius": 9000 - 0.7,
        "ambient": np.array([0.1, 0.1, 0.1]),
        "diffuse": np.array([0.6, 0.6, 0.6]),
        "specular": np.array([1, 1, 1]),
        "shininess": 100,
        "reflection": 0.5,
    },
]

# 여기서부터 실제 광추적
image = np.zeros((height, width, 3))
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        # screen is on origin
        pixel = np.array([x, y, 0])
        origin = camera
        direction = normalize(pixel - origin)

        color = np.zeros((3))
        reflection = 1

        for k in range(max_depth):
            # check for intersections
            nearest_object, min_distance = nearest_intersected_object(
                objects, origin, direction
            )
            if nearest_object is None:
                break

            intersection = origin + min_distance * direction
            normal_to_surface = normalize(intersection - nearest_object["center"])
            shifted_point = intersection + 1e-5 * normal_to_surface
            intersection_to_light = normalize(light["position"] - shifted_point)

            _, min_distance = nearest_intersected_object(
                objects, shifted_point, intersection_to_light
            )
            intersection_to_light_distance = np.linalg.norm(
                light["position"] - intersection
            )
            is_shadowed = min_distance < intersection_to_light_distance

            if is_shadowed:
                break

            illumination = np.zeros((3))

            # ambiant
            illumination += nearest_object["ambient"] * light["ambient"]

            # diffuse
            illumination += (
                nearest_object["diffuse"]
                * light["diffuse"]
                * np.dot(intersection_to_light, normal_to_surface)
            )

            # specular
            intersection_to_camera = normalize(camera - intersection)
            H = normalize(intersection_to_light + intersection_to_camera)
            illumination += (
                nearest_object["specular"]
                * light["specular"]
                * np.dot(normal_to_surface, H) ** (nearest_object["shininess"] / 4)
            )

            # reflection
            color += reflection * illumination
            reflection *= nearest_object["reflection"]

            origin = shifted_point
            direction = reflected(direction, normal_to_surface)

        image[i, j] = np.clip(color, 0, 1)
    # print("%d/%d" % (i + 1, height)) # 성능 잴 때는 출력 제외

plt.imsave("image.png", image)
