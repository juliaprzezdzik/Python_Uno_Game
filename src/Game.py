class Game:
    def __init__(self):
        self.players = [Player("Player 1"), Player("Player 2")]  #lista z graczami  
        self.count_turn = 0 #licznik, czyja jest kolej w grze; zakladamy, ze zawsze zaczyna Player 1 
        self.deck = Deck()
        self.results = [] #zapisywanie poprzednich wynikow rozgrywki 

    def track_turn(self): #count_turn = 0 -> gra Player 1; count_turn = 1 -> gra Player 2 
        self.count_turn = 1 - self.count_turn  

    def save_results(self, result):
        self.results.append(result)

    def reset_game(self): #ponowna inicjalizacja gry 
        self.__init__()
