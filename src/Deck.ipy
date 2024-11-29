import random
from dataclasses import dataclass

#class Card add by Ola
@dataclass
class Card:
    value: str
    color: str

class Deck:
    def __init__(self):
        self.colors = ['Red', 'Green', 'Blue', 'Yellow', 'All']  
        self.numbers = [str(value) for value in range (1,10)]
        self.special_cards = ['Skip', 'Reverse', 'Draw Two']
        self.wild_cards = ['Wild', 'Wild Draw Four']
        self.deck = []
        self.discarded = []
        self.create_deck()

    def create_deck(self):
        for color in self.colors[:-1]:
            self.deck.append(Card('0', color))

            for number in self.numbers:
                for i in range (2):
                    self.deck.append(Card(number, color))
            
            for special_card in self.special_cards:
                for i in range (2):
                    self.deck.append(Card(special_card, color))

        for wild_card in self.wild_cards:
            for _ in range (4):
                self.deck.append(Card(wild_card, self.colors[-1]))

    def shuffle(self):
        random.shuffle(self.deck)

    def is_empty(self):
        if not self.deck:
            return True
        return False
    
    def draw_card(self):
        if(self.is_empty()):
            self.deck = self.discarded[:-2]
            temp = self.discarded[-2]
            self.discarded = []
            self.discarded.append(temp)
            self.shuffle()
        return self.deck.pop()

    def discard_card(self, card):
        self.discarded.append(card)
 
    def display_deck(self):
        for card in self.deck:
            print(f'{card}')

    def display_discarted(self):
        for card in self.discarded:
            print(f'{card}')