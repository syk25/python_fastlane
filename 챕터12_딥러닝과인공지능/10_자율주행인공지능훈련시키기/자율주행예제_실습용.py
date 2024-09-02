""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

from driving_environment import DrivingEnvironment
from ai_driver import DQN
import numpy as np
import argparse
import sys
import random
from collections import namedtuple

Experience = namedtuple("Experience", ("state", "action", "next_state", "reward"))


class ReplayMemory(object):
    def __init__(self):
        self.Q = 0.0  # 훈련에 직접적으로 사용되지 않음
        self.memory = []

    def push(self, *args):
        self.memory.append(Experience(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

    def reset(self):
        self.memory = []


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--mode",
        help="0: AI training, 1: AI replay, 2: Human play",
        type=int,
        default=0,
    )
    parser.add_argument(
        "-f", "--filename", help="PTH filename", type=str, default="00000.pth"
    )
    return parser


def run_interactive_mode(env):

    env.render_fps = 30

    Q_episode = 0.0
    while True:
        user_action, quit_flag = env.process_user_input()
        _, reward, done = env.step(user_action)
        Q_episode = reward + 0.99 * Q_episode
        env.render(tick_fps=env.render_fps, Q_current=Q_episode, Q_max=Q_episode)

        if quit_flag:
            return

        if done:
            env.reset()
            Q_episode = 0.0


def run_replay_mode(env, ai, epsilon=0.0):

    Q_episode = 0.0

    while True:
        _, quit_flag = env.process_user_input()

        action = ai.select_action(env.get_distance_sensors(), epsilon=epsilon)
        _, reward, done = env.step(action)

        Q_episode = reward + ai.gamma * Q_episode

        env.render(tick_fps=30, Q_current=Q_episode, Q_max=Q_episode)

        if quit_flag:
            return

        if done:
            env.reset()
            Q_episode = 0.0


# one episode: 게임 한 판 (시작해서 클리어, 죽을 때 까지, 또는 한계 스텝수 초과)
# epsilon greey로 한 에피소드(episode)를 진행한 후 메모리 반환
def run_episode(env, ai, epsilon, Q_max=0.0):  # Q_max는 화면에 출력하기 위한 용도

    episode_memory = ReplayMemory()

    # TODO:

    while True:

        # 사용자의 게임 조작은 무시하고 프로그램 종료만 확인
        _, quit_flag = env.process_user_input()
        if quit_flag:  # 사용자에 의한 게임 강제 종료
            return episode_memory.Q, quit_flag

        # TODO:

        # 이번 시나리오의 최종 Q 기록. 훈련에 직접적으로 사용되지 않음.
        episode_memory.Q = reward + ai.gamma * episode_memory.Q

        if env.render_mode:
            env.render(
                tick_fps=env.render_fps, Q_current=episode_memory.Q, Q_max=Q_max
            )  # Q_current와 Q_max는 rendering용

        if done:  # 에피소드 종료
            pass  # TODO:

        # TODO:


def run_training_mode(env, ai):

    env.render_fps = 3000

    Q_max = -sys.float_info.max
    epsilon = 0.3
    save_count = 0

    episode_list = []

    while True:

        episode_memory, quit_flag = run_episode(env, ai, epsilon, Q_max)

        if quit_flag:
            return

        episode_list.append(episode_memory)

        # 충분한 경험이 쌓이면 훈련 후 메모리(memory) 리셋
        if len(episode_list) >= 10:

            replay_memory = ReplayMemory()
            for e in episode_list:
                replay_memory.memory += e.memory

            loss = ai.train(replay_memory)

            # 훈련 후 epsilon = 0.0으로 시험 주행
            test_episode_memory, _ = run_episode(env, ai, 0.0, Q_max)

            if test_episode_memory.Q > Q_max:
                Q_max = test_episode_memory.Q
                ai.save(f"{str(save_count).zfill(5)}.pth")  # 네트워크 저장
                save_count += 1

            print(
                f"Current loss = {loss}, Qtest = {test_episode_memory.Q}, Qmax = {Q_max}"
            )

            episode_list = []

            # 테스트 주행 결과가 성공이면 정상 속도(30 fps)로 반복 재생
            if test_episode_memory.memory[-1].reward >= 500.0:
                print("Trained!")
                env.render_mode = True
                env.render_fps = 30
                while True:
                    run_episode(env, ai, 0.0, Q_max)


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()

    env = DrivingEnvironment()

    if args.mode == 2:  # Human play mode
        run_interactive_mode(env)
    else:
        ai = DQN(env.get_distance_sensors().shape[0], env.get_dim_action())
        if args.mode == 0:  # Training mode
            run_training_mode(env, ai)
        elif args.mode == 1:  # Replay mode (PTH filename required)
            ai.load(args.filename)
            run_replay_mode(env, ai)

    env.close()
