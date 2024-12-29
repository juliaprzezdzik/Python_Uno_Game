import matplotlib.pyplot as plt
from collections import deque
import numpy as np
from src.Game import Game
from src.GameState import GameState
from src.Agent import Agent
from src.Action import Action

def train_agent_with_plots(episodes, agent, update_target_every=10):
    rewards = []
    avg_rewards = []
    avg_window = 50
    reward_queue = deque(maxlen=avg_window)
    for episode in range(episodes):
        game = Game()
        game.start_game()
        state = GameState(game).encode_state()
        done = False
        total_reward = 0
        while not done:
            available_actions = [i for i in range(len(game.players[1].cards_in_hand) + 1)]
            action = agent.choose_action(state, available_actions)
            action_class = Action(GameState(game))
            next_game_state, reward, done = action_class.permorm_action(game, action, GameState(game))
            next_state = next_game_state.encode_state()
            agent.store_transition(state, action, reward, next_state, done)
            agent.learn()
            state = next_state
            total_reward += reward
        rewards.append(total_reward)
        reward_queue.append(total_reward)
        avg_rewards.append(np.mean(reward_queue))
        if episode % update_target_every == 0:
            agent.target_net.load_state_dict(agent.Q_eval.state_dict())
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}/{episodes}: Total Reward: {total_reward}, Avg Reward: {avg_rewards[-1]:.2f}")
    plt.figure(figsize=(10, 5))
    plt.plot(rewards, label="Rewards")
    plt.plot(avg_rewards, label=f"Avg Reward (Last {avg_window})", linestyle='--')
    plt.xlabel("Episodes")
    plt.ylabel("Reward")
    plt.title("Training Performance")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    game = Game()
    game.start_game()
    initial_state = GameState(game).encode_state()
    agent = Agent(
        gamma=0.99,
        epsilon=0.9,
        learning_rate=0.00001,
        input_dims=len(initial_state),
        batch_size=64,
        n_actions=108,
        max_mem_size=100000,
        eps_dec=1e-5,
        eps_end=0.01
    )
    train_agent_with_plots(episodes=2000, agent=agent, update_target_every=5)
