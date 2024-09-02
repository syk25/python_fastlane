""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

import torch
import numpy as np
import random
from collections import namedtuple

Experience = namedtuple("Experience", ("state", "action", "next_state", "reward"))


# 재구현이 쉽도록 랜덤 시드 고정
# torch.manual_seed(0)
# random.seed(0)


def make_net(num_input, num_output):
    return torch.nn.Sequential(
        torch.nn.Linear(num_input, 256),
        torch.nn.ReLU(),
        torch.nn.Linear(256, 256),
        torch.nn.ReLU(),
        torch.nn.Linear(256, num_output),
    )


class DQN:  # Deep Q-Learning
    def __init__(self, dim_state, dim_action):
        self.gamma = 0.99
        self.learning_rate = 1e-1
        self.dim_action = dim_action
        self.action_ix = None
        self.prev_loss = None
        self.BATCH_SIZE = 100

        self.policy_net = make_net(dim_state, dim_action)
        self.target_net = make_net(dim_state, dim_action)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = torch.optim.Adam(
            self.policy_net.parameters(), lr=self.learning_rate
        )

    def train(self, replay_memory):

        # 미니 배치를 수동으로 구현 (참고용)
        replay_memory.memory += random.sample(
            replay_memory.memory,
            self.BATCH_SIZE - len(replay_memory) % self.BATCH_SIZE,
        )

        self.num_batches = len(replay_memory) // self.BATCH_SIZE

        for _ in range(1):  # 1 epoch (조절 가능)
            random.shuffle(replay_memory.memory)
            loss_sum = 0.0
            for i in range(0, self.num_batches * self.BATCH_SIZE, self.BATCH_SIZE):
                experience_batch = replay_memory.memory[i : i + self.BATCH_SIZE]
                loss_sum += self.train_batch(experience_batch)

        self.target_net.load_state_dict(self.policy_net.state_dict())

        return loss_sum

    def train_batch(self, experience_batch):

        """
        Pytorch Reinforcement Learning Tutorial
        https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
        """

        batch = Experience(*zip(*experience_batch))

        state_batch = torch.tensor(np.stack([s for s in batch.state]))
        action_batch = torch.tensor(np.stack([torch.tensor([s]) for s in batch.action]))
        reward_batch = torch.tensor(np.stack([torch.tensor(s) for s in batch.reward]))

        non_final_mask = torch.tensor(
            tuple(map(lambda s: s is not None, batch.next_state)), dtype=torch.bool
        )

        non_final_next_states = torch.tensor(
            np.stack([s for s in batch.next_state if s is not None])
        )

        Q_policy = self.policy_net(state_batch).gather(1, action_batch)
        Q_target = self.target_net(non_final_next_states).detach()

        Q_target_max = torch.zeros(self.BATCH_SIZE)
        Q_target_max[non_final_mask] = Q_target.max(1).values

        Q_expected = ((Q_target_max * self.gamma) + reward_batch).unsqueeze(1)

        criterion = torch.nn.MSELoss()
        loss = criterion(Q_policy, Q_expected) / self.num_batches
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return float(loss)

    def select_action(self, state, epsilon):
        if random.random() > epsilon:
            with torch.no_grad():
                state_tensor = torch.from_numpy(state).flatten().unsqueeze(0)
                Q_values_tensor = self.policy_net(state_tensor)
                self.action_ix = int(torch.argmax(Q_values_tensor).numpy())
        else:
            self.action_ix = random.randint(0, self.dim_action - 1)
        return self.action_ix

    def save(self, filename):
        torch.save(self.policy_net, filename)

    def load(self, filename):
        self.policy_net = torch.load(filename)
        self.target_net.load_state_dict(self.policy_net.state_dict())
