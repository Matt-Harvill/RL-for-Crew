from subclasses import *

num_rounds = 10
num_players = 4

def main():

    # Create the game
    game = Game()

    game.players = [Player() for _ in range(num_players)]
    # Assign hands to players
    for player in game.players:
        player.assign_hand(...)

    for i in range(num_rounds):

        # Check for players wanting to reveal

        # Prompt players for a move
        for player in game.players:
            # Check for players wanting to reveal

            color, number = input.split('Type the card you want to play:', ' ')
            player.play_card(Card(color, number))

        # Check if tasks completed or if any can't be completed...

if __name__ == "__main__":
    main()