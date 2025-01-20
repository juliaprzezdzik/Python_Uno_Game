class GameState:
    def __init__(self, game, player_turn = 1):
        self.game = game
        player = game.players[player_turn]
        opponent = game.players[1 - player_turn]
        self.player_cards_count = player.count_cards_in_hand()
        self.opponent_cards_count = opponent.count_cards_in_hand()
        self.cards_in_hands = player.cards_in_hand
        self.current_card = game.deck.get_top_discarded_card()
        self.current_color = self.current_card.color if self.current_card else None
        self.current_value = self.current_card.value if self.current_card else None
        self.special_cards_count = player.count_special_cards()
        self.most_common_color = player.get_most_common_color()
        
    def encode_state(self):
        color_mapping = {"Red" : 0, "Blue" : 1, "Yellow" : 2, "Green" : 3, "All" : 4}
        value_mapping = {"0" : 0, "1" : 1, "2": 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, 
                        "7" : 7, "8" : 8, "9" : 9, "Skip" : 10, "Draw Two" : 11, "Wild" : 12, "Wild Draw Four": 13}      
        current_color = color_mapping.get(self.current_color, -1)
        current_value = value_mapping.get(self.current_value, -1)
        temp_player_hand = [[value_mapping[card.value], color_mapping[card.color]] for card in self.cards_in_hands]
        player_hand = [color_value for card in temp_player_hand for color_value in card]
        most_common_color = color_mapping.get(self.most_common_color, -1)
        
        max_hand_size = 108
        if len(player_hand) < max_hand_size:
            player_hand += [0] * (max_hand_size - len(player_hand))
        else:
            player_hand = player_hand[:max_hand_size]
        
        return [
            self.player_cards_count,
            self.opponent_cards_count,
            self.special_cards_count,
            most_common_color,
            current_color,
            current_value,
            *player_hand
        ]