from game_logic import *
from card import Deck

class Player:
    def __init__(self, name, chip_balance = 1000):
        self.name = name
        self.chip_balance = chip_balance
        self.hand = []
        self.hand_value = 0
        self.split_hand = []
        self.split_hand_value = 0
        self.ace_count = 0
        self.split_ace_count = 0
        self.bet = 0
        self.status = "active"

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