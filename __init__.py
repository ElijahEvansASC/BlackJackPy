from game_logic import Game, GameModifiers

if __name__ == '__main__':
    game_init = GameModifiers()
    print("Game Initiating Modifiers:")
    print(f"Number of Decks: {game_init.deck_number}")
    print(f"Number of Players: {game_init.player_count}")

    game = Game(game_init.deck_number, game_init.player_count, game_init.ruleset)
    print("Game Start:")
    game.start()


