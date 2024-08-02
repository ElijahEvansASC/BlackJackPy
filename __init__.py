from game_logic import Game, GameModifiers

if __name__ == '__main__':
    game_init = GameModifiers()
    print({game_init.deck_number})
    print({game_init.player_count})

    game = Game(game_init.deck_number, game_init.player_count, game_init.ruleset)
    
    print(f"{game.players}")

    game.start()

    print("Players:")
    print(f"{game.players}")
    print("Dealer:")
    print(f"{game.dealer["cards"]}")