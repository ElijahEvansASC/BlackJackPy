class Player:
    def __init__(self, name, chip_count, hand):
        self.name = name
        self.chip_count = chip_count
        self.hand = []

class AIPlayer(Player):
    def __init__(self, name, chip_count, hand, color):
        super().__init__(name, chip_count, hand) #Initializes base class
        self.color = color #New variable of color for AI Player (Red, Blue, Etc.)

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