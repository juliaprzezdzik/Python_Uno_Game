import torch
from torchrl.data import ReplayBuffer, ListStorage
from tensordict import TensorDict
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

class CustomReplayBuffer:
    def __init__(self, max_size, state_dim, n_actions):
        self.storage = ListStorage(max_size=max_size)
        self.buffer = ReplayBuffer(storage=self.storage)
        self.state_dim = state_dim
        self.n_actions = n_actions

    def store_transition(self, state, action, reward, next_state, done):
        transition = TensorDict({
            "state": torch.tensor(state, dtype=torch.float32),
            "action": torch.tensor(action, dtype=torch.float32),
            "reward": torch.tensor(reward, dtype=torch.float32),
            "next_state": torch.tensor(next_state, dtype=torch.float32),
            "done": torch.tensor(done, dtype=torch.bool),
        }, batch_size=[])
        self.buffer.add(transition)

    def sample_buffer(self, batch_size):
        samples = self.buffer.sample(batch_size=batch_size)
        return samples

    def size(self):
        return len(self.storage)

    def get_reward_statistics(self):
        rewards = [transition['reward'].item() for transition in self.storage]
        return {
            'mean': np.mean(rewards),
            'std': np.std(rewards),
            'min': np.min(rewards),
            'max': np.max(rewards)
        }

    def plot_reward_distribution(self):
        rewards = [transition['reward'].item() for transition in self.storage]
        plt.figure(figsize=(10, 6))
        plt.hist(rewards, bins=30, alpha=0.7, edgecolor='black', density=False)
        kde = gaussian_kde(rewards)
        x_vals = np.linspace(min(rewards), max(rewards), 1000)
        plt.plot(x_vals, kde(x_vals) * len(rewards) * (max(rewards) - min(rewards)) / 30, color='red', linewidth=2,
                 label='KDE')
        plt.title('Distribution of rewards')
        plt.xlabel('Reward')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

    def plot_action_distribution(self):
        actions = [transition['action'].item() for transition in self.storage]
        action_counts = {}
        for action in actions:
            action_counts[action] = action_counts.get(action, 0) + 1
        actions_sorted = sorted(action_counts.keys())
        counts_sorted = [action_counts[action] for action in actions_sorted]
        plt.figure(figsize=(10, 6))
        plt.bar(actions_sorted, counts_sorted, color='skyblue', edgecolor='black')
        plt.title('Distribution of actions')
        plt.xlabel('Action')
        plt.ylabel('Number')
        plt.xticks(actions_sorted)
        plt.show()

if __name__ == "__main__":
    buffer = CustomReplayBuffer(max_size=10000, state_dim=4, n_actions=2)
    for _ in range(1000):
        state = np.random.randn(4)
        action = np.random.randint(0, 2)
        reward = np.random.randn()
        next_state = np.random.randn(4)
        done = np.random.choice([True, False])
        buffer.store_transition(state, action, reward, next_state, done)
    stats = buffer.get_reward_statistics()
    print(f"Rewards statistics: {stats}")
    buffer.plot_reward_distribution()
    buffer.plot_action_distribution()
