import pandas as pd
import random
from src.QLearning.Environment import Environment
from Rewards import states, actions

class QLearningAgent:
    def __init__(self, states, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.states = states
        self.actions = actions
        self.environment = environment
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = pd.DataFrame(
            data=0.0, index=pd.MultiIndex.from_tuples(states), columns=actions
        )
        self.q_table.sort_index(inplace=True)
        self.q_table.index.names = [
            "Red Cards", "Green Cards", "Blue Cards", "Yellow Cards",
            "Red Skip", "Green Skip", "Blue Skip", "Yellow Skip",
            "Red Draw Two", "Green Draw Two", "Blue Draw Two", "Yellow Draw Two",
            "Wild", "Wild Draw Four","Top Card Color", "Top Card Value", "Opponent_Cards"
        ]

    def choose_action(self, state):
        valid_actions = [action for action in self.actions if self.environment.is_valid_action(action)]
        if not valid_actions:
            return "Draw Card"
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(valid_actions)
        q_values = self.q_table.loc[state, valid_actions]
        return q_values.idxmax()

    def update_q_value(self, state, action, reward, next_state):
        max_next_q = self.q_table.loc[next_state].max()
        self.q_table.loc[state, action] += self.alpha * (
            reward + self.gamma * max_next_q - self.q_table.loc[state, action]
        )

    def save_q_table_to_csv(self, filename):
        self.q_table.to_csv(filename)
        print(f"Q-table saved to {filename}")

    def train(self, episodes, environment, save_interval=100, filename="q_table.csv"):
        for episode in range(episodes):
            self.epsilon = max(0.1, self.epsilon * 0.99)
            state = environment.reset()
            done = False
            total_reward = 0
            steps = 0
            # max_steps = 1000
            # while not done and steps < max_steps:
            steps += 1
            action = self.choose_action(state)
            next_state, reward, done = environment.step(action)
            self.update_q_value(state, action, reward, next_state)
            state = next_state
            total_reward += reward
            # if steps == max_steps:
            #     print(f"Warning: Episode {episode} reached maximum steps!")
            if episode % save_interval == 0:
                self.save_q_table_to_csv(filename)
                print(f"Episode {episode}/{episodes}, Total Reward: {total_reward}, Epsilon: {self.epsilon:.4f}")
        self.save_q_table_to_csv(filename)
        print(f"Training complete. Q-table saved to {filename}")

if __name__ == "__main__":
    possible_states, states_dict = states(sample_size=100)
    possible_actions = actions()
    environment = Environment(possible_states, possible_actions)
    agent = QLearningAgent(
        states=possible_states,
        actions=possible_actions,
        alpha=0.9,
        gamma=0.9,
        epsilon=0.9
    )
    agent.train(episodes=10000, environment=environment, save_interval=100, filename="q_table.csv")