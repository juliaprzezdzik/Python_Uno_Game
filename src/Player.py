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
        s = ''
        for i, card in enumerate(self.cards_in_hand):
            s += f"[{i+1}] {card.color} {card.value}"
            if i < len(self.cards_in_hand) - 1:
                s += ', '
        return s
    
    def count_cards_in_hand(self):
        return len(self.cards_in_hand)
