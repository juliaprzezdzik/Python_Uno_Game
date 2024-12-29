import random
from src.Deck import Card
from src.Game import Game

class Environment:
    def __init__(self, states, actions):
        self.states = states
        self.actions = actions
        self.current_state = None
        self.colors = ["Red", "Green", "Blue", "Yellow"]
        self.values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Draw Two", "Wild", "Wild Draw Four"]
        self.game = Game()

    def reset(self):
        self.current_state = random.choice(self.states)
        return self.current_state

    def is_valid_action(self, action):
        top_card_color = self.colors[self.current_state[-3]]
        top_card_value = self.values[self.current_state[-2]]
        if action.startswith("Play"):
            action_parts = action.split()
            card_color = action_parts[1]
            card_value = " ".join(action_parts[2:]) if len(action_parts) > 2 else "0"
            card = Card(value=card_value, color=card_color)
            top_card = Card(value=top_card_value, color=top_card_color)
            return self.game.is_valid_move(card, top_card)
        elif action == "Draw Card":
            return True
        return False

    def step(self, action):
        if not self.is_valid_action(action):
            reward = -20
            print(f"Invalid action: {action}, Current state: {self.current_state}")
            return self.current_state, reward, False
        next_state = random.choice(self.states)
        total_cards_in_hand = sum(self.current_state[:4]) + sum(self.current_state[4:8])
        opponent_cards = self.current_state[-1]
        reward = 0
        if total_cards_in_hand == 0:
            reward = 10
        elif opponent_cards == 0:
            reward = -10
        elif opponent_cards == 1:
            if "Draw Two" in action or "Draw Four" in action:
                reward = 3
            else:
                reward = -1
        elif opponent_cards <= 2:
            if "Draw Two" in action or "Wild Draw Four" in action:
                reward = 2
        if total_cards_in_hand == 1:
            reward += 3
        reward += max(0, 5 - total_cards_in_hand)
        if action == "Draw Card":
            reward -= 1
        elif action == "Play Wild":
            reward += 0.6
        elif action == "Play Wild Draw Four":
            reward += 1.5
        elif "Draw Two" in action:
            reward += 0.7
        elif "Skip" in action:
            reward += 2
        self.current_state = next_state
        done = total_cards_in_hand == 0 or opponent_cards == 0
        print(f"Action: {action}, Reward: {reward}, Done: {done}, Next state: {next_state}")
        return next_state, reward, done