from Deck import Deck, Card

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
            self.cards_in_hand.remove(card)
            return card
        else:
            return None
            
    def if_uno(self):
        return len(self.cards_in_hand) == 1
        
    def sort_cards_in_hand(self):
        self.cards_in_hand.sort(key=lambda card: (card.color, card.value))
    
    def display_cards_in_hand(self):
        card_descriptions = [f"[{i+1}] {card.color} {card.value}" for i, card in enumerate(self.cards_in_hand)]
        return ', '.join(card_descriptions)
    
    def count_cards_in_hand(self):
        return len(self.cards_in_hand)
    
    def count_special_cards(self):
        special_counts = {"Skip" : 0, "Draw Two" : 0, "Wild Draw Four" : 0, "Wild" : 0}
        for card in self.cards_in_hand:
            if card.value in special_counts:
                special_counts[card.value] += 1
        total = sum(special_counts.values())
        return total
    
    def count_color(self):
        color_counts = {"Red" : 0, "Blue" : 0, "Green" : 0, "Yellow" : 0, "All" : 0}

        for card in self.cards_in_hand:
            if card.color in color_counts:
                color_counts[card.color] += 1
        self.color_counts = color_counts
        return color_counts
    
    def get_most_common_color(self):
        color = self.count_color()
        return max(color, key=color.get)
