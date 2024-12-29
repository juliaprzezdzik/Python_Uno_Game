import torch
from torchrl.data import ReplayBuffer, ListStorage
from tensordict import TensorDict

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