import torch
from torchrl.data import ReplayBuffer, ListStorage
from tensordict import TensorDict
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.stats import gaussian_kde

class CustomReplayBuffer:
    def __init__(self, max_size, state_dim, n_actions):
        self.storage = ListStorage(max_size=max_size)
        self.buffer = ReplayBuffer(storage=self.storage)
        self.state_dim = state_dim
        self.n_actions = n_actions

    def store_transition(self, state, action, reward, next_state, done, priority=1.0):
        transition = TensorDict({
            "state": torch.tensor(state, dtype=torch.float32),
            "action": torch.tensor(action, dtype=torch.float32),
            "reward": torch.tensor(reward, dtype=torch.float32),
            "next_state": torch.tensor(next_state, dtype=torch.float32),
            "done": torch.tensor(done, dtype=torch.bool),
            "priority": torch.tensor(priority, dtype=torch.float32)
        }, batch_size=[])
        self.buffer.add(transition)

    def sample_buffer(self, batch_size):
        samples = self.buffer.sample(batch_size=batch_size)
        return samples

    def size(self):
        return len(self.storage)

    def sample_with_priority(self, batch_size, alpha=0.6):
        if len(self.storage) == 0:
            raise ValueError("Buffer is empty.")
        priorities = [transition["priority"].item() for transition in self.storage]
        probabilities = [p ** alpha for p in priorities]
        total_prob = sum(probabilities)
        probabilities = [p / total_prob for p in probabilities]
        indices = random.choices(range(len(self.storage)), weights=probabilities, k=batch_size)
        sampled_transitions = [self.storage[idx] for idx in indices]
        result = {
            "states": torch.stack([t["state"] for t in sampled_transitions]),
            "actions": torch.stack([t["action"] for t in sampled_transitions]),
            "rewards": torch.stack([t["reward"] for t in sampled_transitions]),
            "next_states": torch.stack([t["next_state"] for t in sampled_transitions]),
            "dones": torch.stack([t["done"] for t in sampled_transitions]),
            "indices": indices
        }
        return result

    def update_priorities(self, indices, new_priorities):
        for idx, prio in zip(indices, new_priorities):
            self.storage[idx]["priority"] = torch.tensor(prio, dtype=torch.float32)

if __name__ == "__main__":
    buffer = CustomReplayBuffer(max_size=10000, state_dim=4, n_actions=2)
    for _ in range(1000):
        state = np.random.randn(4)
        action = np.random.randint(0, 2)
        reward = np.random.randn()
        next_state = np.random.randn(4)
        done = np.random.choice([True, False])
        buffer.store_transition(state, action, reward, next_state, done, priority=1.0)
    stats = buffer.get_reward_statistics()
    print(f"Rewards statistics: {stats}")
    buffer.plot_reward_distribution()
    buffer.plot_action_distribution()
    buffer.visualize_rewards_distribution()
    buffer.visualize_transitions(num_samples=3)
    batch_size = 5
    samples_priority = buffer.sample_with_priority(batch_size=batch_size, alpha=0.6)
    print("Sampled transitions (priority-based): ")
    for i in range(batch_size):
        print(f"Transition {i + 1}, Reward = {samples_priority['rewards'][i].item():.2f}, "
              f"Priority = {buffer.storage[samples_priority['indices'][i]]['priority'].item():.2f}")
    new_priorities = [abs(samples_priority['rewards'][i].item()) + 0.01 for i in range(batch_size)]
    buffer.update_priorities(samples_priority['indices'], new_priorities)
    print("\nUpdated priorities based on absolute reward + 0.01")
    for i, idx in enumerate(samples_priority['indices']):
        print(f"Index {idx}, new priority = {buffer.storage[idx]['priority'].item():.2f}")
