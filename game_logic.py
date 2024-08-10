from utils import InputValidateAndSanitize as ivs
from card import Deck
from player import Colors, Player, AIPlayer

class Payouts:
    def standard(bet_amount):
        winnings = bet_amount
        payout = winnings + bet_amount
        return payout

    def natural_blackjack(bet_amount):
        winnings = bet_amount * 1.5
        payout = winnings + bet_amount
        return payout
    
    def insurance(bet_amount):
        winnings = bet_amount * 2
        payout = winnings
        return payout
    
    def push(bet_amount):
        winnings = 0
        payout = winnings + bet_amount
        return payout
    
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

        #Dictionary for User
        players["You"] = Player(name = "You") 

        for i in range(1, player_count):
            color_name = colors[i % len(colors)]  # Modulo avoids index error
            players[f"{color_name} Player"] = AIPlayer(name=f"{color_name} Player", is_dealer = False)

        return players
    
    def initialize_dealer(self):
        #Dictionary for dealer
        dealer = AIPlayer(name="Dealer", is_dealer = True)
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
    def __init__(self, deck, players, dealer, min_bet=5, max_bet=500):
        self.deck = deck
        self.players = players
        self.dealer = dealer
        self.min_bet = min_bet
        self.max_bet = max_bet

    def deal_initial_cards(self):
        num_initial_cards = 2

        for _ in range(num_initial_cards):
            for player_name in self.players:
                player = self.players[player_name]
                card = self.deck.deal(1)[0]
                player.hand.append(card)

            card = self.deck.deal(1)[0]
            self.dealer.hand.append(card)

    def place_initial_bets(self):
        for player_name in self.players:
            player = self.players[player_name]
            if hasattr(player, 'AI'):
                self.AI_betting_logic(player)
            else:
                self.betting_prompt(player)

    def natural_blackjack_check(self):
        # Output status of hands after initial deal
        print(f"Your Hand: {self.players['You'].hand}")
        print(f"Dealer's Face Up Card: {self.dealer.hand[0]}")

        dealer_upcard = self.dealer.hand[0]
        if dealer_upcard.rank == "A":
            print("Insurance Bet Logic")
            self.game_round_logic()
        else:
            for player_name in self.players:
                player = self.players[player_name]
                player.hand_value = self.calculate_hand_value(player.hand)
                if player.hand_value == 21:
                    print(f"{player.name} has a natural blackjack!")
                    player.status = 'inactive'
                    player.chip_balance += Payouts.natural_blackjack(player.bet)
                    print(player.chip_balance)
                    print(player.hand)
            self.game_round_logic()

    def game_round_logic(self):
        dealer_bust = False

        # Process each player's turn
        for player_name in self.players:
            player = self.players[player_name]
            if player.status == 'active':
                if hasattr(player, 'AI'):
                    self.AI_round_decision_logic(player)
                else:
                    self.round_decision(player)

        # Process Dealer's turn
        while self.calculate_hand_value(self.dealer.hand) < 17:
            self.hit(self.dealer)
            if self.dealer.hand_value > 21:
                dealer_bust = True
                self.dealer.status = "inactive"
                print("Dealer has gone bust!")
                break

        # Determine the outcome of the round
        if dealer_bust:
            for player_name in self.players:
                player = self.players[player_name]
                if player.status == 'active':
                    player.chip_balance += Payouts.standard(player.bet)
        else:
            for player_name in self.players:
                player = self.players[player_name]
                if player.status == 'active':
                    self.player_win_decision(player, self.dealer)

    def AI_round_decision_logic(self, player):
        while player.hand_value < 17:
            self.hit(player)
            player.hand_value = self.calculate_hand_value(player.hand)
        self.player_bust_determination(player)

    def round_decision(self, player):
        choices = ['h', 'st', 'dd', 'sp']
        valid_choice = False
    
        while not valid_choice:
            player_decision = input("Enter 'st' to stand, 'h' to hit, 'dd' to double down, or 'sp' to split: ").strip().lower()
        
            if player_decision in choices:
                validated_player_decision = player_decision
                valid_choice = True
            else:
                print("That is not an acceptable option. Please try again.")
    
    # Proceed with the valid choice
        if validated_player_decision == 'st':
            self.stand(player)
        elif validated_player_decision == 'h':
            self.hit(player)
            player.hand_value = self.calculate_hand_value(player.hand)
            self.player_bust_determination(player)
        elif validated_player_decision == 'dd':
            self.double_down(player)
        elif validated_player_decision == 'sp':
            print('Player Split Logic.')


    def betting_prompt(self, player):
        while True:
            player.bet = input("Enter your betting amount in multiples of 5. Min bet of $5, Max bet of $500:")
            player.bet = ivs.is_num_input(player.bet)
            if player.bet is not None and self.min_bet <= player.bet <= self.max_bet and player.bet % 5 == 0:
                player.chip_balance -= player.bet
                print(f'{player.name} bets ${player.bet}.')
                return player.bet
            else:
                print(f"Bet must be between ${self.min_bet} and ${self.max_bet} and in multiples of 5.")

    def AI_betting_logic(self, player):
        player.bet = self.min_bet
        player.chip_balance -= player.bet
        print(f'{player.name} bets ${player.bet}.')

    def hit(self, player):
        print(f'{player.name} draws a card.')
        card = self.deck.deal(1)[0]
        player.hand.append(card)
        player.hand_value = self.calculate_hand_value(player.hand)  # Update hand value

    def stand(self, player):
        print(f"{player.name} stands.")

    def double_down(self, player):
        player.chip_balance -= player.bet
        player.bet *= 2
        self.hit(player)
        self.player_bust_determination(player)

    def player_bust_determination(self, player):
        if player.hand_value > 21:
            player.status = "inactive"
            print(f"{player.name} has busted!")

    def calculate_hand_value(self, cards):
        hand_value = 0
        num_aces = 0
        for card in cards:
            if card.rank in ['J', 'Q', 'K']:
                hand_value += 10
            elif card.rank == 'A':
                hand_value += 11
                num_aces += 1
            else:
                hand_value += int(card.rank)

        while hand_value > 21 and num_aces:
            hand_value -= 10
            num_aces -= 1
        return hand_value

    def player_win_decision(self, player, dealer):
        if player.hand_value > dealer.hand_value:
            print(f"{player.name} wins with a hand of {player.hand_value} to {dealer.hand_value}.")
            player.chip_balance += Payouts.standard(player.bet)
        elif player.hand_value < dealer.hand_value:
            print(f"{player.name} loses with a hand of {player.hand_value} to {dealer.hand_value}.")
        else:
            print(f"{player.name} has a push with the dealer, no winner.")
            player.chip_balance += player.bet
#====================
    def start(self):
        #Place Initial bet
        self.place_initial_bets()
        #Deal Initial Cards.
        self.deal_initial_cards()
        #If dealer up card is an Ace, reveal second card after insurance bet OR check for players if they have a natural blackjack.
        self.natural_blackjack_check()
        #Else, Prompt each player for an action.
        self.game_round_logic()
        #At the end of all player actions, reveal cards and calculate wins and losses
        print('Round over.')
        #Prompt to leave table if desired
        #Restart the game loop.