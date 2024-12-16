# !! wstepna wersja ReplayBuffer - jeszcze nie zintegrowana z projektem !!!!

import torch
from torchrl.data import ReplayBuffer, ListStorage
from tensordict import TensorDict

class CustomReplayBuffer:
    def __init__(self, max_size, state_dim, n_actions):
        """
        max_size - maksymalny rozmiar bufora
        state_dim - wymiary stanu (ile informacji opisuje stan w grze)
        n_actions - liczba możliwych akcji
        """
        self.storage = ListStorage(max_size=max_size)  # lista do przechowywania dsowiadczen
        self.buffer = ReplayBuffer(storage=self.storage)
        self.state_dim = state_dim
        self.n_actions = n_actions

    def store_transition(self, state, action, reward, next_state, done):
        #TensorDict przechowuje dane jednego kroku agenta
        transition = TensorDict({
            "state": torch.tensor(state, dtype=torch.float32), #aktualny stan gry
            "action": torch.tensor(action, dtype=torch.float32), #akcja, ktora agent wykonal
            "reward": torch.tensor(reward, dtype=torch.float32), # nagroda za akcje
            "next_state": torch.tensor(next_state, dtype=torch.float32), #stan po akjcji
            "done": torch.tensor(done, dtype=torch.bool), #czy gra sie skonczyla
        }, batch_size=[])

        # dodawanie doświadczenie do bufora
        self.buffer.add(transition)

    def sample_buffer(self, batch_size):
        """
        losowe probkowanie z bufora
        batch_size - liczba próbek do pobrania
        zwraca losowe próbki w formie TensorDict
        """
        samples = self.buffer.sample(batch_size=batch_size)
        return samples
