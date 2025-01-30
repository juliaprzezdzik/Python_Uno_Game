import random
from .Environment import Environment
import matplotlib.pyplot as plt
import h5py
import numpy as np

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def get_q(self, state, action):
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        return self.q_table[state].get(action, 0.0)

    def choose_action(self, state, valid_actions):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(valid_actions)
        q_values = [self.get_q(state, a) for a in valid_actions]
        max_q = max(q_values)
        actions_with_max_q = [a for a, q in zip(valid_actions, q_values) if q == max_q]
        return random.choice(actions_with_max_q)

    def update_q_value(self, state, action, reward, next_state, next_valid_actions):
        current_q = self.get_q(state, action)
        if next_valid_actions:
            max_next_q = max([self.get_q(next_state, a) for a in next_valid_actions])
        else:
            max_next_q = 0
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        self.q_table[state][action] = new_q

    def save_q_table_to_h5(self, filename):
        try:
            states = []
            actions = []
            q_values = []
            for state, actions_dict in self.q_table.items():
                state_str = '|'.join(map(str, state))
                for action, value in actions_dict.items():
                    states.append(state_str)
                    actions.append(action)
                    q_values.append(value)
            states_np = np.array(states, dtype='S')
            actions_np = np.array(actions, dtype='S')
            q_values_np = np.array(q_values, dtype='float32')
            with h5py.File(filename, 'w') as h5file:
                h5file.create_dataset('states', data=states_np, compression='gzip', compression_opts=4)
                h5file.create_dataset('actions', data=actions_np, compression='gzip', compression_opts=4)
                h5file.create_dataset('q_values', data=q_values_np, compression='gzip', compression_opts=4)
            print(f"Q-table saved to {filename}")
        except Exception as e:
            print(f"Failed to save Q-table to {filename}: {e}")

    def load_q_table_from_h5(self, filename):
        try:
            with h5py.File(filename, 'r') as h5file:
                states = h5file['states'][:].astype(str)
                actions = h5file['actions'][:].astype(str)
                q_values = h5file['q_values'][:]
                self.q_table = {}
                for state, action, value in zip(states, actions, q_values):
                    state_tuple = tuple(map(int, state.split('|')))
                    if state_tuple not in self.q_table:
                        self.q_table[state_tuple] = {}
                    self.q_table[state_tuple][action] = value
            print(f"Q-table loaded from {filename}")
        except Exception as e:
            print(f"Failed to load Q-table from {filename}: {e}")

def train_agents(episodes, environment, agent_A, agent_B, save_interval=100, filename_A="q_table_A.h5", filename_B="q_table_B.h5"):
    rewards_A = []
    rewards_B = []
    max_steps = 1000
    for episode in range(1, episodes + 1):
        agent_A.epsilon = max(0.1, agent_A.epsilon * 0.99)
        agent_B.epsilon = max(0.1, agent_B.epsilon * 0.99)
        state = environment.reset()
        done = False
        total_rewards = {0: 0, 1: 0}
        steps = 0
        while not done and steps < max_steps:
            steps += 1
            acting_player = environment.current_player
            current_agent = agent_A if acting_player == 0 else agent_B
            valid_actions = [action for action in environment.action_space if environment.is_valid_action(action)]
            if not valid_actions:
                action = "Draw Card"
            else:
                action = current_agent.choose_action(state, valid_actions)
            next_state, reward, done, actual_player = environment.step(action)
            total_rewards[actual_player] += reward
            next_valid_actions = [a for a in environment.action_space if environment.is_valid_action(a)]
            current_agent.update_q_value(state, action, reward, next_state, next_valid_actions)
            state = next_state
        rewards_A.append(total_rewards[0])
        rewards_B.append(total_rewards[1])
        if episode % save_interval == 0:
            agent_A.save_q_table_to_h5(filename_A)
            agent_B.save_q_table_to_h5(filename_B)
            print(f"Episode {episode}/{episodes}, Steps: {steps}, Rewards: A={total_rewards[0]}, B={total_rewards[1]}")
    agent_A.save_q_table_to_h5(filename_A)
    agent_B.save_q_table_to_h5(filename_B)
    print(f"Training complete. Q-tables saved for both agents.")
    plot_rewards(rewards_A, rewards_B)

def plot_rewards(rewards_A, rewards_B):
    plt.figure(figsize=(10, 6))
    plt.plot(rewards_A, label="Agent A Rewards", color='blue')
    plt.xlabel("Episodes")
    plt.ylabel("Total Rewards")
    plt.title("Rewards per Episode for Agent A")
    plt.legend()
    plt.grid()
    plt.savefig("agent_a_rewards.png")
    plt.show()
    plt.figure(figsize=(10, 6))
    plt.plot(rewards_B, label="Agent B Rewards", color='green')
    plt.xlabel("Episodes")
    plt.ylabel("Total Rewards")
    plt.title("Rewards per Episode for Agent B")
    plt.legend()
    plt.grid()
    plt.savefig("agent_b_rewards.png")
    plt.show()

if __name__ == "__main__":
    environment = Environment()
    agent1 = QLearningAgent(
        actions=environment.action_space,
        alpha=0.1,
        gamma=0.9,
        epsilon=1.0
    )
    agent2 = QLearningAgent(
        actions=environment.action_space,
        alpha=0.1,
        gamma=0.9,
        epsilon=1.0
    )
    train_agents(10000, environment, agent1, agent2)