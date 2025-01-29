from src.Deck import Card, Deck
from src.Player import Player
import logging
import random
from src.DQN.Agent import Agent
from src.DQN.GameState import GameState
import numpy as np

logging.basicConfig(level=logging.INFO)

class Game:
    def __init__(self):
        self.players = [Player("Player 1"), Player("Player 2")] 
        self.count_turn = 0
        self.deck = Deck()
        self.results = []
        self.bonus_number_of_cards_to_draw = 0
        self.next_player_takes_cards = False
        self.skip = False
        self.is_color_changed = False

    def track_turn(self):
        if self.skip:
            self.skip = False
            return
        self.count_turn = 1 - self.count_turn

    def save_results(self, result):
        self.results.append(result)

    def reset_game(self):
        self.__init__()

    def deal_cards(self, num_cards):
        for player in self.players:
            for _ in range(num_cards):
                if not self.deck.is_empty():
                    player.draw_card(self.deck)
            player.sort_cards_in_hand()
    
    def is_valid_move(self, card, top_card):
        if self.next_player_takes_cards:
            if card.value in ["Wild Draw Four","Draw Two"]:
                return True
            else:
                return False
        else:
            return top_card.color == "All" or card.color == "All" or card.color == top_card.color or card.value == top_card.value

    def is_deck_empty(self):
        return self.deck.is_empty()

    def draw_card(self,player_index):
        player = self.players[player_index]
        for _ in range( 1 + self.bonus_number_of_cards_to_draw):
            player.draw_card(self.deck)
        player.sort_cards_in_hand()
        self.bonus_number_of_cards_to_draw = 0
        self.next_player_takes_cards = False

    def play_card(self, player_index, card_index):
        player = self.players[player_index]
        top_card = self.deck.get_top_discarded_card()
        card = player.cards_in_hand[card_index]
        if self.is_valid_move(card, top_card):
            self.last_played_card = top_card
            player.throw_card(card_index, self.deck)
            if card.value == "Draw Two":
                self.bonus_number_of_cards_to_draw += 2
                self.next_player_takes_cards = True
            if card.value == "Wild Draw Four":
                self.bonus_number_of_cards_to_draw += 4
                self.is_color_changed = True
                self.next_player_takes_cards = True
            if card.value == "Skip":
                self.skip = True
            if card.value == "Wild":
                self.is_color_changed = True
            return True
        else:
            return False
        
    def change_color(self, color):
        card = self.deck.get_top_discarded_card()
        card.color = color
        self.is_color_changed = False

    def start_game(self, initial_hand_size=7):
        self.reset_game()
        self.deck.shuffle()
        self.deal_cards(initial_hand_size)
        first_card = self.deck.get_first_card()
        self.last_played_card = first_card
        self.deck.discard_card(first_card)

    def check_winner(self):
        for player in self.players:
            if len(player.cards_in_hand) == 0:
                return player
        return None
    
    def take_your_turn(self):
        logging.info("Your cards: ")
        logging.info(self.players[0].display_cards_in_hand())
        logging.info("Which card do you want to play?")
        number = int(input("Type number of card (from 1 to {x}) or 0 if you want to draw a card: ".format(x=self.players[0].count_cards_in_hand())))
        return number - 1

    def random_move(self, player_index=1):
        for i in range(self.players[player_index].count_cards_in_hand()):
            if self.play_card(player_index, i):
                if self.is_color_changed:
                    color = random.choice(self.deck.colors[:-1])
                    self.change_color(color)
                return
        self.draw_card(player_index)

    def bot_move(self, agent, player_index=1):
        state = GameState(self).encode_state()
        available_actions = self.check_playable_cards(player_index=1)
        action = agent.choose_action(state, available_actions)
        if action < len(self.players[player_index].cards_in_hand):
            self.play_card(player_index, action)
            if self.is_color_changed:
                self.change_color(self.players[1].get_most_common_color())
        else:
            self.draw_card(player_index)


    def check_playable_cards(self, player_index):
        available_actions = []
        available_cards = []
        current_card = self.deck.get_top_discarded_card()
        for index, card in enumerate(self.players[player_index].cards_in_hand):
            if ((current_card.value == "Draw Two" or current_card.value == "Wild Draw Four") and self.next_player_takes_cards):
                if card.value == "Draw Two" or card.value == "Wild Draw Four":
                    available_actions.append(index)
                    available_cards.append([index, card])  
            elif card.value == self.deck.get_top_discarded_card().value or card.color == self.deck.get_top_discarded_card().color or card.value in self.deck.wild_cards:
                available_actions.append(index)
                available_cards.append([index, card])
        available_actions.append(len(self.players[player_index].cards_in_hand))
        available_cards.append([len(self.players[player_index].cards_in_hand), "DRAW CARD"])
        return available_actions
