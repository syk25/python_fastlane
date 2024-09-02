""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

import numpy as np
import pygame
from pygame.locals import *
from PIL import Image


class DrivingEnvironment:
    def __init__(self, simple_mode=True, scenario=0):

        # simple_mode에서는 Action space의 차원이 3
        # 일반 모드에서는 5
        self.simple_mode = simple_mode

        pygame.init()

        self.screen = pygame.display.set_mode((1280, 960))  # 윈도우 크기
        self.clock = pygame.time.Clock()
        self.scenario = scenario

        track_filename = "track.png" if scenario == 0 else "track2.png"

        self.track = pygame.image.load(track_filename).convert()
        self.track = pygame.transform.scale(self.track, self.screen.get_size())

        collision_map = (
            Image.open(track_filename).resize(self.screen.get_size()).convert("RGB")
        )
        collision_map = np.asarray(collision_map)[:, :, 2]
        collision_map = np.where(collision_map == 0, 0, 255)

        self.pygame = pygame
        self.collision_map = collision_map
        self.img = pygame.image.load("redcar40x70.png").convert_alpha()

        self.font1 = pygame.font.SysFont("system", 40)
        self.font2 = pygame.font.SysFont("system", 30)

        self.turn_coeff = 0.5
        self.accel_coeff = 0.15
        self.fric = 0.02

        self.reset()
        self.step(4)

        self.render_mode = True

    def reset(self):
        self.dir = self.pygame.Vector2(1.0, 0.0)
        self.speed = 0.0
        self.up = self.pygame.Vector2(0.0, -1.0)  # 차 이미지의 초기 앞 방향
        self.angle = self.dir.angle_to(self.up)  # 차체의 회전

        self.center = (
            self.pygame.Vector2(120, 580)
            if self.scenario == 0
            else self.pygame.Vector2(500, 450)
        )

        self.travel_distance = 0.0

        # 몸체 센서들의 위치 (자동차 좌표계)
        self.body_sensors_local = (
            self.pygame.Vector2(-20, -35),
            self.pygame.Vector2(0, -35),
            self.pygame.Vector2(20, -35),
            self.pygame.Vector2(20, 0),
            self.pygame.Vector2(20, 35),
            self.pygame.Vector2(0, 35),
            self.pygame.Vector2(-20, 35),
            self.pygame.Vector2(-20, 0),
        )
        # 몸체 센서 상태 (0: 도로 위 정상, 그외: 도로 밖 비정상)
        self.body_sensors_status = np.zeros(len(self.body_sensors_local))

        # 거리 센서
        self.sensing_radius = 150.0
        self.distance_sensors_status = np.ones(
            360 // 30, dtype=np.float32
        )  # 감지된 거리 [0, 1]
        # 거리 센서들의 방향 (자동차 좌표계)
        self.distance_sensors_dir_local = tuple(
            self.up.rotate(a)
            for a in range(0, 360, 360 // self.distance_sensors_status.shape[0])
        )

        # 몸체가 어딘가에 충돌했을 때 True
        # 이 flag를 이용해서 게임 fail 조건 확인
        self.collision_flag = False

        self.frame_count = 0

    def step(self, action):

        # 한 번에 한 행위(action)만 가능 입력 가능
        if self.simple_mode:
            if action == 0:
                self.turn_left()
            elif action == 1:
                self.turn_right()
        else:
            if action == 0:
                self.turn_left()
            elif action == 1:
                self.turn_right()
            elif action == 2:
                self.decel()
            elif action == 3:
                self.accel()

        # 자동차의 상태
        if self.simple_mode:
            self.speed = 5.0  # 심플 모드에서는 항상 직진
        else:
            self.speed *= 1.0 - self.fric  # 바닥 마찰

        self.center += self.dir * self.speed
        self.travel_distance += self.speed  # 원래 이동 거리는 속력 * 시간간격이지만 시간간격은 1.0이라고 단순화

        # 몸체 센서
        self.angle = self.dir.angle_to(self.up)
        self.body_sensors_global = tuple(
            x.rotate(-self.angle) + self.center for x in self.body_sensors_local
        )

        self.collision_flag = False
        for i, s in enumerate(self.body_sensors_global):
            self.body_sensors_status[i] = self.check(s)
            if not self.check(s):
                self.collision_flag = True  # 센서 중 하나만 충돌해도 True

        # 거리 센서
        self.distance_sensors_dir_global = tuple(
            x.rotate(-self.angle) for x in self.distance_sensors_dir_local
        )

        # 거리 감지
        if not self.check(self.center):
            self.distance_sensors_status.fill(0.0)
        else:
            dt = 0.2
            for i, d in enumerate(self.distance_sensors_dir_global):
                t = dt
                while t < 1.0:
                    c = self.center + (t + dt) * self.sensing_radius * d
                    # print(c, self.check(c))
                    if self.check(c):
                        t += dt
                    else:
                        t = self.search(self.center, d, t, t + dt, 5)
                        break
                self.distance_sensors_status[i] = t

        self.frame_count += 1

        reward = self.speed
        done = False  # 게임을 종료해야할 때 True

        if self.collision_flag or (self.center[0] < 10 and self.scenario == 0):
            reward = -500.0
            done = True

        # 시나리오 0 결승선 통과
        if self.scenario == 0 and self.center[0] > 1100:
            reward = 500.0
            done = True  # 완주 시 게임 종료

        # 시나리오 1 두 바퀴 완주
        if self.scenario == 1 and self.travel_distance > 6000.0:
            reward = 500.0
            done = True

        # 계속 멈춰있을 경우에도 실격으로 종료
        if self.frame_count > 10 and self.speed < 1e-1:
            reward = -500.0
            done = True

        # 너무 오래 지속되는 경우 중단
        if self.frame_count > 5000:
            done = True

        return self.get_distance_sensors(), reward, done

    def draw_car(self, screen):

        # 자동차 몸체
        img_rotated = self.pygame.transform.rotate(self.img, self.angle)
        rect = img_rotated.get_rect()
        rect.center = self.center
        screen.blit(img_rotated, rect)

        # 자동차 테두리
        self.pygame.draw.polygon(
            screen,
            (255, 120, 120),
            self.body_sensors_global,
            width=1,
        )

        # 자동차 몸체 센서들
        for i, c in enumerate(self.body_sensors_global):
            if not self.body_sensors_status[i]:  # 길 밖으로 나감
                self.pygame.draw.circle(screen, (255, 0, 0), c, radius=5, width=0)
            else:
                self.pygame.draw.circle(screen, (0, 255, 0), c, radius=2, width=0)

        # 자동차 거리 센서들
        for i, d in enumerate(self.distance_sensors_dir_global):
            dist_global = self.distance_sensors_status[i] * self.sensing_radius
            self.pygame.draw.line(
                screen,
                (130, 130, 130),
                self.center,
                self.center + d * self.sensing_radius,
                width=1,
            )
            self.pygame.draw.line(
                screen,
                (255, 255, 100),
                self.center,
                self.center + d * dist_global,
                width=1,
            )

    # c가 길 위에 있으면 True, 아니면 False
    def check(self, c):
        try:
            return self.collision_map[int(c[1]), int(c[0])] == 0
        except IndexError:
            return False

    def search(self, center, direction, t1, t2, count):
        # assert self.check(t1) == True and self.check(t2) == False

        if count == 0:
            return t1
        tm = (t1 + t2) * 0.5
        if self.check(center + tm * self.sensing_radius * direction):
            return self.search(center, direction, tm, t2, count - 1)
        else:
            return self.search(center, direction, t1, tm, count - 1)

    def accel(self):
        self.speed += self.accel_coeff

    def decel(self):
        self.speed -= self.accel_coeff

    def turn_left(self):
        self.dir.rotate_ip(-self.turn_coeff * self.speed)

    def turn_right(self):
        self.dir.rotate_ip(self.turn_coeff * self.speed)

    def render(self, tick_fps=30, Q_current=0.0, Q_max=0.0):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.track, (0, 0))

        self.draw_car(self.screen)

        # Finish line
        if self.scenario == 0:
            self.pygame.draw.line(
                self.screen, (255, 255, 255), (1100, 0), (1100, 1280), width=1
            )

        speed_text = self.font1.render(
            f"Speed = {self.speed:.1f}, Collision = {self.collision_flag}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(speed_text, (450, 30))

        dist_text = ""
        for i in range(self.distance_sensors_status.shape[0]):
            d = self.distance_sensors_status[i]
            dist_text += f"{d:.1f} "

        self.screen.blit(self.font2.render(dist_text, True, (255, 255, 255)), (430, 80))

        Q_max_text = (
            f"Qmax = {max(0.0, Q_max):.1f}" if Q_max > -1000.0 else "Qmax = -INF"
        )
        self.screen.blit(
            self.font1.render(Q_max_text, True, (255, 255, 255)), (200, 20)
        )
        Q_current_text = f"Q = {Q_current:.1f}"
        self.screen.blit(
            self.font1.render(Q_current_text, True, (255, 255, 255)), (200, 50)
        )

        frame_text = f"Frame = {self.frame_count}"
        self.screen.blit(
            self.font1.render(frame_text, True, (255, 255, 255)), (200, 80)
        )

        # Flip the display
        self.pygame.display.flip()
        self.clock.tick(tick_fps)

    def process_user_input(self):
        quit_flag = False
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                quit_flag = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.render_mode = not self.render_mode

        keys = self.pygame.key.get_pressed()

        action = 4

        if keys[K_LEFT]:
            action = 0
        elif keys[K_RIGHT]:
            action = 1
        elif keys[K_DOWN] and not self.simple_mode:
            action = 2
        elif keys[K_UP] and not self.simple_mode:
            action = 3

        return action, quit_flag

    def get_dim_action(self):
        if self.simple_mode:
            return 3  # 좌, 우, 아무것도 안함
        else:
            return 5  # 좌, 우, 감속, 가속, 아무것도 안함

    def close(self):
        pygame.quit()

    def get_distance_sensors(self):
        return self.distance_sensors_status.copy()
