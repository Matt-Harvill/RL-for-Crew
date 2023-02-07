from game import Game

def main():

    # Create the game
    game = Game(num_bots=0)

    # Initialize the game (assign hands and tasks)
    game.initialize()

    # Start the game
    game.play()

if __name__ == "__main__":
    main()