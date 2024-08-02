from utils import InputValidateAndSanitize as ivs
from card import Deck
from player import Colors
#Add input validation logic within the class
class GameModifiers:
    def __init__(self):
        self.deck_number = self.deck_input()
        self.player_count = self.player_input()
        self.ruleset = self.ruleset()
    #Valid deck choices are one, or multiples of two up to eight decks.
    #While an exit condition is not met (while True), the loop will continue to prompt for input.
    #The function validates and sanitizes the user entry, and breaks the loop if the choice is in the valid_deck_choices array.
    def deck_input(self):
        valid_deck_choices = [1, 2, 4, 6, 8]
        while True:
            deck_number = input("Choose decks in play from 1, 2, 4, 6 or 8:")
            deck_choice = ivs.is_num_input(deck_number)
            if deck_choice is not None and deck_choice in valid_deck_choices:
                return deck_choice
            else:
                print("That is not a valid number of decks. Please choose 1, 2, 4, 6 or 8 decks.")
    
    #Similar logic to GameModifiers.deck_input() function.
    def player_input(self):
        valid_player_choices = [1, 2, 3, 4, 5, 6, 7]
        while True:
            player_number = input("Choose player count from 1-7 players:")
            player_choice = ivs.is_num_input(player_number)
            if player_choice is not None and player_choice in valid_player_choices:
                return player_choice
            else:
                print("That is not a valid number of players. Please choose a number 1 through 7.")
    
    def ruleset(self):
        ruleset = "Standard"
        return ruleset


class Game:
    def __init__(self, deck_number, player_count, ruleset):
        self.deck_number = deck_number
        self.player_count = player_count
        self.ruleset = ruleset
        self.players = self.initialize_players(player_count)
        self.dealer = self.initialize_dealer()
        self.deck = Deck(deck_number)
        self.initialize_game()

    def initialize_players(self, player_count):
        #Dictionary for players
        players = {}
        colors = Colors.get_colors() #Gets list of colors

        for i in range(1, player_count):
            color_name = colors[i % len(colors)] #Modulo avoids index error
            players[f"{color_name} Player"] = {
                "chips" : 1000, #Initial chip count
                "bet": 0, #Initial bet amount
                "cards": [], #initial empty card list
                "status": "active"
            }

        #Dictionary for User
        players["You"] = {
                "chips" : 1000, #Initial chip count
                "bet": 0, #Initial bet amount
                "cards": [], #initial empty card list
                "status": "active"
        }

        return players
    
    def initialize_dealer(self):
        #Dictionary for dealer
        dealer = {
            "cards": [],
            "status": "waiting"
        }
        return dealer
    
    def initialize_game(self):
        #If the ruleset is standard, creates an instance of a standard game and stores it in self.game
        if self.ruleset == "Standard":
            self.game = StandardGame(self.deck, self.players, self.dealer)
        else:
            raise ValueError("Unsupported ruleset")
    
    #Starts the game that is intialized in the initialize_game(self) function
    def start(self):
        if hasattr(self, 'game'):
            self.game.start() #Start the game by calling the start method of StandardGame
        else:
            raise RuntimeError("Game not initialized.")
            
class StandardGame:
    def __init__(self, deck, players, dealer):
        self.deck = deck
        self.players = players
        self.dealer = dealer
    
    def deal_initial_cards(self):
        num_initial_cards = 2 #Number of initial cards dealt.
        for _ in range(num_initial_cards): #For the integer in the range of the value stored in num_initial_cards, repeat the loop (Twice).
            for player in self.players:
                card = self.deck.deal(1)[0]
                self.players[player]["cards"].append(card)

            card = self.deck.deal(1)[0]
            self.dealer["cards"].append(card)

        

    def start(self):
        #Deal Initial Cards.
        self.deal_initial_cards()
        #Remaining Game Logic.