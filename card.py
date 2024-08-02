import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self, deck_number):

        self.deck_number = deck_number
        self.cards = self._create_deck()
        self.shuffle()

    def _create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [Card(rank, suit) for suit in suits for rank in ranks] * self.deck_number

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        #While the number of cards is greater than the length of the deck, extend the deck by creating a new deck
        while num_cards > len(self.cards):
            self.cards.extend(self._create_deck())
            self.shuffle()

        dealt_cards = [self.cards.pop() for _ in range(num_cards)]
        return dealt_cards
    
    #Gives the remaining number of cards in the deck
    def __len__(self):
        return len(self.cards)
    #Gives a string representation of the deck
    def __repr__(self):
        return ', '.join(map(str, self.cards))

        


