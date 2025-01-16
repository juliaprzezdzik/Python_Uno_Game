import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim 

class DQN(nn.Module):
    def __init__(self, learning_rate, input_size, layer1_size, layer2_size, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(input_size, layer1_size)
        self.layer2 = nn.Linear(layer1_size, layer2_size)
        self.layer3 = nn.Linear(layer2_size, n_actions)
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.optimizer = optim.Adam(self.parameters(), lr = learning_rate)
        self.loss = nn.MSELoss()
        self.to(self.device)

    def forward(self, state):
        x = F.relu(self.layer1(state))
        x = F.relu(self.layer2(x))
        actions = self.layer3(x)
        return actions
