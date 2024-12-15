import torch as T
import numpy as np
from Model import DQN

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
        self.memory_counter = 0
        self.Q_eval = DQN(self.learning_rate, n_actions=n_actions, input_size=input_dims, layer1_size=256, layer2_size=256)
        self.state_memory = np.zeros((self.mem_size, input_dims), dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, input_dims), dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool_)

    def store_transition(self, state, action, reward, new_stage, done):
        index = self.memory_counter % self.mem_size 
        self.state_memory[index] = state
        self.new_state_memory[index] = new_stage
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = done
        self.memory_counter += 1

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
        if self.memory_counter < self.batch_size:
            return 
        self.Q_eval.optimizer.zero_grad()
        max_mem = min(self.memory_counter, self.mem_size)
        batch = np.random.choice(max_mem, self.batch_size, replace=False)
        batch_index = np.arange(self.batch_size, dtype=np.int32)
        state_batch = T.tensor(self.state_memory[batch]).to(self.Q_eval.device)
        new_state_batch = T.tensor(self.new_state_memory[batch]).to(self.Q_eval.device)
        reward_batch = T.tensor(self.reward_memory[batch]).to(self.Q_eval.device)
        terminal_batch = T.tensor(self.terminal_memory[batch]).to(self.Q_eval.device)
        action_batch = T.tensor(self.action_memory[batch], dtype=T.long).to(self.Q_eval.device)
        q_eval = self.Q_eval.forward(state_batch)[batch_index, action_batch]
        q_next = self.Q_eval.forward(new_state_batch)
        q_next[terminal_batch] = 0.0
        q_target = reward_batch + self.gamma * T.max(q_next, dim=1)[0]
        loss = self.Q_eval.loss(q_target, q_eval).to(self.Q_eval.device)
        loss.backward()
        self.Q_eval.optimizer.step()
        self.epsilon = self.epsilon - self.eps_dec if self.epsilon > self.eps_min else self.eps_min


