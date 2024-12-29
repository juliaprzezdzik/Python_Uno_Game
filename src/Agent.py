import torch as T
import numpy as np
from src.Model import DQN
from src.ReplayBuffer import CustomReplayBuffer

class Agent():
    def __init__(self, gamma, epsilon, learning_rate, input_dims, batch_size, 
                 n_actions, max_mem_size=100000, eps_end=0.01, eps_dec = 5e-4):
        self.gamma = gamma
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.eps_min = eps_end 
        self.eps_dec = eps_dec
        self.action_space = [i for i in range(n_actions)]
        self.mem_size = max_mem_size 
        self.batch_size = batch_size
        self.Q_eval = DQN(self.learning_rate, n_actions=n_actions, input_size=input_dims, layer1_size=256, layer2_size=256)
        self.replay_buffer = CustomReplayBuffer(max_size=max_mem_size, state_dim=input_dims, n_actions=n_actions)

    def store_transition(self, state, action, reward, new_stage, done):
        self.replay_buffer.store_transition(state, action, reward, new_stage, done)

    def choose_action(self, state, available_actions):
        state = T.tensor(state, dtype=T.float32).to(self.Q_eval.device)
        actions = self.Q_eval.forward(state.unsqueeze(0))
        mask = T.full(actions.size(), -float('inf'), device=self.Q_eval.device)
        mask[0, available_actions] = 0
        masked_actions = actions + mask
        random = np.random.random()
        if random > self.epsilon:
            action_idx = T.argmax(masked_actions).item() 
        else:
            action_idx = np.random.choice(available_actions)
        return action_idx

    def learn(self):
        if self.replay_buffer.size() < self.batch_size:
            return
        samples = self.replay_buffer.sample_buffer(self.batch_size)
        states = samples["state"]
        actions = samples["action"].long()
        rewards = samples["reward"]
        next_states = samples["next_state"]
        dones = samples["done"]
        q_eval = self.Q_eval.forward(states)[range(self.batch_size), actions]
        q_next = self.Q_eval.forward(next_states).max(dim=1)[0]
        q_next[dones] = 0.0
        q_target = rewards + self.gamma * q_next
        loss = self.Q_eval.loss(q_target, q_eval).to(self.Q_eval.device)
        loss.backward()
        self.Q_eval.optimizer.step()
        self.epsilon = max(self.eps_min, self.epsilon - self.eps_dec)