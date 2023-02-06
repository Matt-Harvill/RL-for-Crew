from subclasses import Player, Task
import numpy as np

class Game(object):

    def __init__(self, num_bots):
        
        assert num_bots <= 3
        self.num_players = 3
        self.num_bots = num_bots
        self.num_humans = self.num_players - self.num_bots
        self.num_unique_tasks = 5
        self.task_assignments = {} # Player : Task

        self.players = []

        self.total_rounds = 13
        self.num_rounds_complete = None
        self.captain = None
        self.start_player_idx = None # idx of player who starts the round

        # initialize players
        for i in range(self.num_players):
            if i < self.num_bots:
                player = Player(is_agent = True, id = i)
            else:
                player = Player(is_agent = False, id = i)
            
            self.players.append(player)


        # initialize tasks (sample 2 from the 5 total)

        self.tasks = np.random.choice(list(range(self.num_unique_tasks)), size = 2, replace = False)

        self.tasks = [Task(i) for i in self.tasks]

        # initialize deck

        self.deck = []
        for color in ["G", "P", "Y", "B", "SUB"]:
            for num in range(1,10):
                if color == "SUB" and num > 4:
                    break
                self.deck.append(Card(color, num))

        self.deck = np.random.shuffle(self.deck)


        
    def initialize(self):
        # assign hands, sample tasks

        # assume there is three players
        assert self.num_players == 3

        # ensure that no one player always gets the largest hand
        self.players = np.shuffle(self.players)

        self.players[0].assign_hand[self.deck[:13]]

        self.players[1].assign_hand[self.deck[13:27]]

        self.players[2].assign_hand[self.deck[27:]]

        # assign captain

        for idx, player in enumerate(self.players):
            for card in self.cards_in_hand:
                if card == Card("SUB", 4):
                    self.captain = player
                    self.start_player_idx = idx
                    break

        assert self.captain != None



    def show_hands(self):

        for idx, player in enumerate(self.players):

            print(f"Player {idx}, your hand is: ")

            for card in player.cards_in_hand():


    def share_info_window(self):

    def play_card_window(self, player):

        print(f"Player {idx}, choose one card to play")
        print(player.get_printable_hand())

        valid = False
        card_to_play = None

        while not valid:
            received = input()

            if not is_instance(received, int):
                print("Invalid input")
                continue
            
            card_to_play = player.cards_in_hand[received]

            # make sure valid card is played
            if not (self.trump == None or card_to_play.color == self.trump or \
             self.trump not in [color for card.color for card in player.cards_in_hand]):
                print("You must play the same color as trump if you have it in your hand")
  
            else:
                valid = True

        player.play_card(card_to_play)

        self.trick.append(card_to_play)
 

    def check_trick_winner(self):

        winner = None
        curr_highest_num = 0
        for player, played_card in self.curr_trick:
            if played_card.color == self.trump and played_card.number > curr_highest_num:
                winner = player
                curr_highest_num = played_card.number
            elif played_card.color == "SUB":
                self.trump = "SUB"
                curr_highest_num = played_card.number
                winner = player

        return player

        

    def play(self):

        self.initialize()

        print("Begin game!")

        # show each player their hand via terminal
        self.show_hands()
        
        
        for round in range(self.total_rounds):

            curr_player_idx = self.start_player_idx

            self.curr_trick = {} # player : played_card

            for i in range(num_players):
                # allow players to show information
                self.share_info_window()

                # allow each current player to play
                curr_player = self.players[curr_player_idx]

                played_card = self.play_card_window(curr_player)

                self.curr_trick[curr_player] = played_card

                if i == 0: # if start of the round, assign the trump color
                    self.trump = played_card.color

                curr_player_idx = (curr_player_idx + 1) % self.num_players
    

            # award one player the trick and set them to start the next round

            winner = self.check_trick_winner()
            self.start_player_idx = winner.id

            game_status = self.get_game_status()

            if game_status == "lost":
                print("Lost game")

            elif game_status == "done":
                print("Ya'll won! Go celebrate w boba")



    def get_game_status(self):

        completed_tasks = 0
        for player, task in self.task_assignments:
            task.update_completion(self, player)
            if task.is_complete:
                completed_tasks += 1
            elif task.is_impossible:
                return "lost"

        if completed_tasks == 2:
            return "won"

        return "ongoing"


        


        

        
