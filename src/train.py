from src.Game import Game
from src.GameState import GameState
from src.Agent import Agent
from src.Action import Action

def train_agent(episodes, agent):
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
            reward = action_class.permorm_action(game, action, GameState(game))
            next_state = GameState(game).encode_state()
            done = game.check_winner() is not None
            agent.store_transition(state, action, reward, next_state, done)
            agent.learn()
            state = next_state
            total_reward += reward
        print(f"Epizod {episode} : Wynik: {total_reward}")

if __name__ == "__main__":
    game = Game()
    game.start_game()
    initial_state = GameState(game).encode_state()
    agent = Agent(
        gamma = 0.99,
        epsilon = 1.0,
        learning_rate = 0.00001,
        input_dims = len(initial_state),
        batch_size=64,
        n_actions = 108,
        max_mem_size = 100000,
        eps_dec = 1e-4,
        eps_end = 0.01
    )
    train_agent(episodes=2000, agent=agent)