import torch
from torchrl.data import ReplayBuffer, ListStorage
from tensordict import TensorDict
import random

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
