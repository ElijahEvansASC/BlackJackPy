from game_logic import *
from card import Deck

class Player:
    def __init__(self, name, chip_balance = 1000):
        self.name = name
        self.chip_balance = chip_balance
        self.hand = []
        self.split_hand = []
        self.bet = 0
        self.status = "active"

    def initial_bet(self, amount):
        if amount <= self.chip_balance:
            self.bet = amount
            self.chip_balance -= amount
        else:
            raise ValueError("Insufficient chip balance to bet this amount.")
        
    def draw_card(self, card):
        self.hand.append(card)
    
    def draw_split_card(self, card):
        self.split_hand.append(card)

    def reset(self):
        self.bet = 0
        self.hand = []
        self.split_hand = []
        self.status = "active"

class AIPlayer(Player):
    def __init__(self, name, is_dealer, initial_chips=1000):
        super().__init__(name, initial_chips)
        self.AI = True
        self.is_dealer = is_dealer

    def AI_game_logic():
        print("AI Game Logic Here.")

class Colors:
    #Class attributes
    colors = ['Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan']
    ansi_colors = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m']

    @classmethod
    def get_colors(cls):
        return cls.colors
    
    @classmethod
    def get_ansi_colors(cls):
        return cls.ansi_colors
    
class PlayerStatus:
    status = ['active', 'doubling-down', 'folding', 'splitting', 'standing', 'busted', 'win', 'loss']