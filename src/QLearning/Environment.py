from src.Deck import Card
from src.Game import Game
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

class Environment:
    def __init__(self):
        self.game = Game()
        self.current_player = 0
        self.action_space = self.define_actions()

    @staticmethod
    def define_actions():
        colors = ["Red", "Green", "Blue", "Yellow"]
        values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Draw Two"]
        possible_actions = []
        for color in colors:
            for value in values:
                possible_actions.append(f"Play {color} {value}")
        for color in colors:
            possible_actions.append(f"Play Wild {color}")
            possible_actions.append(f"Play Wild Draw Four {color}")
        possible_actions.append("Draw Card")
        return possible_actions

    def reset(self, test_setup=False):
        if test_setup:
            self.game.reset_game()
            self.game.players[0].cards_in_hand = [
                Card("Draw Two", "Green"),
                Card("5", "Red"),
                Card("Wild", "All")
            ]
            self.game.players[1].cards_in_hand = [
                Card("3", "Yellow"),
                Card("4", "Blue")
            ]
            self.game.deck.discarded = [Card("3", "Green")]
            self.current_player = 0
        else:
            self.game.start_game(initial_hand_size=7)
            self.current_player = 0
        logging.info("Game reset.")
        logging.info(f"Player 0 hand: {[f'{card.value} {card.color}' for card in self.game.players[0].cards_in_hand]}")
        logging.info(f"Player 1 hand: {[f'{card.value} {card.color}' for card in self.game.players[1].cards_in_hand]}")
        logging.info(f"Discarded pile: {[f'{card.value} {card.color}' for card in self.game.deck.discarded]}")
        return self.get_state()

    def get_state(self):
        player = self.game.players[self.current_player]
        opponent = self.game.players[1 - self.current_player]
        top_card = self.game.deck.get_top_discarded_card()
        if top_card:
            logging.info(f"Top card color: {top_card.color}, value: {top_card.value}")
        else:
            logging.info("No top card.")
        state = (
            len(player.cards_in_hand),
            len(opponent.cards_in_hand),
            self.color_to_num(top_card.color) if top_card else 4,
            self.value_to_num(top_card.value) if top_card else 14,
            int(any(card.value == "Skip" for card in player.cards_in_hand)),
            int(any(card.value == "Draw Two" for card in player.cards_in_hand)),
            int(any(card.value == "Wild" for card in player.cards_in_hand)),
            int(any(card.value == "Wild Draw Four" for card in player.cards_in_hand))
        )
        logging.info(f"Generated state: {state}")
        logging.info(f"------------------------")
        return state

    @staticmethod
    def color_to_num(color):
        color_mapping = {
            "Red": 0,
            "Green": 1,
            "Blue": 2,
            "Yellow": 3,
            "All": 4
        }
        num = color_mapping.get(color, 4)
        return num

    @staticmethod
    def value_to_num(value):
        value_mapping = {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "Skip": 10,
            "Draw Two": 11,
            "Wild": 12,
            "Wild Draw Four": 13,
            "None": 14
        }
        num = value_mapping.get(value, 14)
        return num

    def is_valid_action(self, action):
        agent = self.game.players[self.current_player]
        top_card = self.game.deck.get_top_discarded_card()
        card, _ = self.action_to_card(action, agent)
        return self.game.is_valid_move(card, top_card) if card else action == "Draw Card"

    @staticmethod
    def action_to_card(action, player):
        if action.startswith("Play Wild"):
            parts = action.split()
            if len(parts) == 3:
                wild_type = parts[1]
                chosen_color = parts[2]
                for card in player.cards_in_hand:
                    if card.value == wild_type:
                        return card, chosen_color
        elif action.startswith("Play"):
            parts = action.split()
            if len(parts) >= 3:
                color = parts[1]
                value = " ".join(parts[2:])
                for card in player.cards_in_hand:
                    if card.color == color and card.value == value:
                        return card, None
        elif action == "Draw Card":
            return None, None
        return None, None

    def calculate_reward(self, agent, card, chosen_color):
        reward = 0
        if card.value == "Draw Two":
            reward += 0.7
            if self.should_use_draw_two(agent, card):
                reward += 1
            else:
                reward -= 0.5
        elif card.value == "Wild Draw Four":
            reward += 1.5
            if self.should_use_wild_draw_four(agent, card):
                reward += 2
            else:
                reward -= 0.7
        elif card.value == "Skip":
            reward += 2
        elif card.value == "Wild":
            reward += 0.6
            if self.should_use_wild(agent, card, chosen_color):
                reward += 1
            else:
                reward -= 0.5
        else:
            reward += max(0, 5 - len(agent.cards_in_hand))
        if len(agent.cards_in_hand) == 1:
            reward += 3
        if card.value in ["Wild", "Wild Draw Four"] and chosen_color:
            self.game.change_color(chosen_color)
            if self.should_use_wild(agent, card, chosen_color):
                reward += 1
            else:
                reward -= 0.5
        if len(agent.cards_in_hand) > 10:
            reward -= 5
        color_counts = {"Red": 0, "Green": 0, "Blue": 0, "Yellow": 0}
        for card in agent.cards_in_hand:
            if card.color in color_counts:
                color_counts[card.color] += 1
        most_common_color_count = max(color_counts.values())
        reward += 0.1 * most_common_color_count
        return reward

    def should_use_draw_two(self, agent, card):
        agent_card_count = len(agent.cards_in_hand)
        opponent_card_count = len(self.game.players[1 - self.current_player].cards_in_hand)
        return agent_card_count > 5 and opponent_card_count <= 3

    def should_use_wild_draw_four(self, agent, card):
        agent_card_count = len(agent.cards_in_hand)
        opponent_card_count = len(self.game.players[1 - self.current_player].cards_in_hand)
        return agent_card_count > 5 and opponent_card_count <= 3

    @staticmethod
    def should_use_wild(agent, card, chosen_color, majority_threshold=2):
        color_counts = {"Red": 0, "Green": 0, "Blue": 0, "Yellow": 0}
        for c in agent.cards_in_hand:
            if c.color in color_counts:
                color_counts[c.color] += 1
        optimal_color = max(color_counts, key=color_counts.get)
        max_count = color_counts[optimal_color]
        sorted_counts = sorted(color_counts.values(), reverse=True)
        if len(sorted_counts) < 2:
            second_max_count = 0
        else:
            second_max_count = sorted_counts[1]
        if (max_count - second_max_count) >= majority_threshold:
            return chosen_color == optimal_color
        else:
            return False

    def step(self, action, max_steps=1000):
        acting_player = self.current_player
        agent = self.game.players[acting_player]
        reward = 0
        valid = False
        if action == "Draw Card":
            self.game.draw_card(acting_player)
            reward = -1
            valid = True
        else:
            card, chosen_color = self.action_to_card(action, agent)
            if card is not None:
                card_index = agent.cards_in_hand.index(card)
                if self.game.play_card(acting_player, card_index):
                    valid = True
                    reward += self.calculate_reward(agent, card, chosen_color)
                    if card.value in ["Wild", "Wild Draw Four"] and chosen_color:
                        self.game.change_color(chosen_color)
                    if len(agent.cards_in_hand) == 1:
                        reward += 3
                    if self.game.next_player_takes_cards:
                        self.game.draw_card(1 - acting_player)
                else:
                    reward = -30
            else:
                reward = -30
        if len(agent.cards_in_hand) < 5:
            reward += 0.2
        done = self.game.check_winner() is not None
        if done:
            winner = self.game.check_winner()
            if winner == agent:
                steps_bonus = max_steps - self.game.count_turn
                reward += 10 + steps_bonus * 0.1
            else:
                reward -= 10 + (max_steps - self.game.count_turn) * 0.1
        if not done and valid:
            self.game.track_turn()
            self.current_player = 1 - acting_player
        next_state = self.get_state()
        return next_state, reward, done, acting_player