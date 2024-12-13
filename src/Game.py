from Deck import Card, Deck
from Player import Player
import logging
import random

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
    
    def is_valid_move(self, card, top_card):
        if self.next_player_takes_cards == True:
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
        self.bonus_number_of_cards_to_draw = 0
        self.next_player_takes_cards = False

    def play_card(self, player_index, card_index):
        player = self.players[player_index]
        top_card = self.deck.get_top_discarded_card()
        card = player.cards_in_hand[card_index]

        if self.is_valid_move(card, top_card):
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

    def random_move(self):
        for i in range(self.players[1].count_cards_in_hand()):
            if self.play_card(1, i):
                if self.is_color_changed:
                    color = random.choice(self.deck.colors[:-1])
                    self.change_color(color)
                return
        self.draw_card(1)           
    
if __name__ == "__main__":
    game = Game()
    game.start_game()
    while game.check_winner() == None:
        print("The top of the stack: ")
        print(game.deck.get_top_discarded_card())
        print("Your turn!")
        while True:
            result = game.take_your_turn()
            if result == -1:
                game.draw_card(0)
                print("You drew a card.\n")
                break
            elif game.play_card(0, result):
                print("You played '{played_card}'.\n".format(played_card=game.deck.get_top_discarded_card()))
                break
        print("The top of the stack: ")
        print(game.deck.get_top_discarded_card())
        print("My turn!")
        if game.random_move():
            print("I played '{played_card}'.\n".format(played_card=game.deck.get_top_discarded_card()))
        else:
            game.draw_card(1)
            print("I drew a card.\n")
    if game.check_winner == game.players[0]:
        print("You won!")
    else:
        print("I won!")
