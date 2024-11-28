class Game:
    def __init__(self):
        self.players = [Player("Player 1"), Player("Player 2")] 
        self.count_turn = 0
        self.deck = Deck()
        self.results = []
        self.ilosc_kart_do_dobrania = 1
        self.next_player_takes_cards = False

    def track_turn(self):
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
        if top_card.value in ["Draw Two", "Wild Draw Four"] and self.next_player_takes_cards == True:
            if card.value in ["Wild Draw Four","Draw Two"]:
                return True
            else:
                return False
        return top_card.color == "All" or card.color == "All" or card.color == top_card.color or card.value == top_card.value

    def is_deck_empty(self):
        return self.deck.is_empty()

    def take_card(self,player_index):
        player = self.players[player_index]
        for _ in range(self.ilosc_kart_do_dobrania):
            player.draw_card(self.deck)
        self.ilosc_kart_do_dobrania = 1
        self.next_player_takes_cards = False

    def play_card(self, player_index, card_index):
        player = self.players[player_index]
        top_card = self.deck.get_top_discarded_card()
        card = player.cards_in_hand[card_index]

        if self.is_valid_move(card, top_card):
            player.throw_card(card_index, self.deck)
            if card.value == "Draw Two":
                self.ilosc_kart_do_dobrania += 2
            if card.value == "Wild Draw Four":
                self.ilosc_kart_do_dobrania += 4
            return True
        else:
            return False

    def start_game(self, initial_hand_size=7):
        self.reset_game()
        self.deck.shuffle()
        self.deal_cards(initial_hand_size)
        first_card = self.deck.draw_card()
        self.deck.discard_card(first_card)

    def check_winner(self):
        for player in self.players:
            if len(player.cards_in_hand) == 0:
                return player
        return None
                    
