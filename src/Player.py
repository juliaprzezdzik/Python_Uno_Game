class Player:
    def __init__(self, name):
        self.name = name
        self.cards_in_hand = []
        
    def draw_card(self, deck):
        card = deck.draw_card()
        self.cards_in_hand.append(card)

    def throw_card(self, card_index, deck):
        card = self.cards_in_hand[card_index]
        if card:
            deck.discard_card(card)
            self.last_played_card = card
            self.cards_in_hand.remove(card)
            return card
        else:
            return None
            
    def if_uno(self):
        return len(self.cards_in_hand) == 1

    def if_last_move(self):
        return len(self.cards_in_hand) == 2

    def sort_cards_in_hand(self):
        self.cards_in_hand.sort(key=lambda card: (card.color, card.value))
    
    def display_cards_in_hand(self):
        card_descriptions = [f"[{i+1}] {card.color} {card.value}" for i, card in enumerate(self.cards_in_hand)]
        return ', '.join(card_descriptions)
    
    def count_cards_in_hand(self):
        return len(self.cards_in_hand)
    
    def count_skip_cards(self):
        colour_count = {"Red" : 0, "Blue" : 0, "Green" : 0, "Yellow" : 0}
        for card in self.cards_in_hand:
            if card.value == "Skip":
                colour_count[card.color] += 1
        return sum(colour_count.values())
    
    def count_special_cards(self):
        special_counts = {"Skip" : 0, "Draw Two" : 0, "Wild Draw Four" : 0, "Wild" : 0}
        for card in self.cards_in_hand:
            if card.value in special_counts:
                special_counts[card.value] += 1
        total = sum(special_counts.values())
        return total
    
    def count_wild_cards(self):
        return sum([1 for card in self.cards_in_hand if card.value in ["Wild Draw Four", "Wild"]])

   
    def count_color(self):
        color_counts = {"Red" : 0, "Blue" : 0, "Green" : 0, "Yellow" : 0}

        for card in self.cards_in_hand:
            if card.color in color_counts:
                color_counts[card.color] += 1
        self.color_counts = color_counts
        return color_counts
    
    def get_most_common_color(self):
        color = self.count_color()
        return max(color, key=color.get)

    def count_cards_with_same_value(self):
        value_counts = {}
        for card in self.cards_in_hand:
            if card.value in value_counts:
                value_counts[card.value] += 1
            else:
                value_counts[card.value] = 1
        return value_counts

    def count_identical_cards(self, card):
        return sum([1 for card2 in self.cards_in_hand if card2.value == card.value and card2.color == card.color])
