from subclasses import Player, Task, Card
from typing import List
import numpy as np
import readline # Allows for navigating through previous user inputs

class Game:

    def __init__(self, num_bots):
        
        # Can't be more than 3 bots
        assert num_bots <= 3

        self.num_players = 3
        self.num_bots = num_bots
        self.num_humans = self.num_players - self.num_bots
        self.num_unique_tasks = 5
        self.task_assignments = {} # Player : Task

        self.players = []

        self.total_rounds = 13
        self.num_rounds_complete = 0
        self.captain = None
        self.start_player_idx = None # idx of player who starts the round
        self.trump_color = None

        # initialize players
        for i in range(self.num_players):
            if i < self.num_bots:
                player = Player(is_agent = True, id = i)
            else:
                player = Player(is_agent = False, id = i)
            
            self.players.append(player)

        # initialize tasks (sample 2 from the 5 total)
        task_idx_to_str = {0: 'less_than_captain', 1: 'no_green_no_yellow', 2: 'exactly_2_tricks', \
            3: 'win_using_a_6', 4: 'win_green5_blue8'}

        tasks_idxs = np.random.choice(list(range(self.num_unique_tasks)), size = 2, replace = False)

        self.tasks = [Task(task_idx_to_str[i]) for i in tasks_idxs]

        # initialize deck
        deck = []
        for color in ['green', 'pink', 'yellow', 'blue', 'sub']:
            for num in range(1,10):
                if color == 'sub' and num > 4:
                    break
                deck.append(Card(color, num))

        np.random.shuffle(deck)
        self.deck = list(deck)


        
    def initialize(self):
        # assign hands, sample tasks

        # assume there is three players
        assert self.num_players == 3

        # ensure that no one player always gets the largest hand
        np.random.shuffle(self.players)
        self.players: List['Player'] = list(self.players)
        self.players[0].assign_hand(self.deck[:13])
        self.players[1].assign_hand(self.deck[13:26])
        self.players[2].assign_hand(self.deck[26:])

        # assign captain
        captain_card = Card('sub', 4)
        player: 'Player'
        for idx, player in enumerate(self.players):
            card: 'Card'
            for card in player.cards_in_hand:
                if card == captain_card:
                    self.captain = player
                    self.start_player_idx = idx
                    break
        assert self.captain != None

        

    def show_hands(self) -> None:
        '''
        Print all of the players' hands
        '''
        player: 'Player'
        for idx, player in enumerate(self.players):
            print(f'Player {idx}, your hand is: {player.get_printable_hand()}')
        print()

    def share_info_window(self):
        player: 'Player'
        for idx, player in enumerate(self.players):
            # Check if player wants to share info
            correct_y_n_input = False
            while not correct_y_n_input:
                share_info = input(f'Player {idx}, your hand is: {player.get_printable_hand()} \
                    \nDo you want to share info? [y/n]\n')
                correct_y_n_input = (share_info == 'y' or share_info == 'n')
                if not correct_y_n_input:
                    print('Please type \'y\' or \'n\'\n')

            # If player said yes then get their info
            if share_info == 'y':
                success_sharing = False
                while not success_sharing:
                    shared_info = input(f'Player {idx}, your hand is: {player.get_printable_hand()} \
                        \nWhat info do you want to share? \
                        \nFormat is \'position color number\' \
                        \nValid positions: lowest, only, highest \
                        \nValid colors: yellow, green, blue, pink \
                        \nValid numbers: 1-9\n').split(' ')
                    # Make sure input has three arguments
                    if len(shared_info) != 3:
                        print('\nIncorrect format, please try again\n')
                        continue
                    else:
                        success_sharing = player.share_info(Card(shared_info[1], int(shared_info[2])), shared_info[0])
        print()

    def play_card_window(self, player: 'Player') -> 'Card':

        success_playing_card = False

        while not success_playing_card:
            card_to_play_input = input(f'Player {player.id}, choose one card to play \
                \nHere is your hand: {player.get_printable_hand()}\n').split(' ')

            if len(card_to_play_input) != 2:
                print('\nIncorrect format, please try again\n')
                continue
            else:
                card_to_play = Card(card_to_play_input[0], int(card_to_play_input[1]))
                success_playing_card = player.play_card(self, card_to_play)

        # Card was successfully played
        card_played = card_to_play
        return card_played
 

    def check_trick_winner(self):

        winner = None
        curr_highest_num = 0

        player: 'Player'
        played_card: 'Card'
        print(self.curr_trick)
        for player, played_card in self.curr_trick.items():
            if played_card.color == self.trump_color and played_card.number > curr_highest_num:
                winner = player
                curr_highest_num = played_card.number
            elif played_card.color == 'sub':
                self.trump_color = 'sub'
                curr_highest_num = played_card.number
                winner = player

        return winner

        

    def play(self):

        self.initialize()

        print('Begin game!')

        # show each player their hand via terminal
        self.show_hands()
        
        for round in range(self.total_rounds):

            curr_player_idx = self.start_player_idx

            self.curr_trick = {} # player : played_card

            for i in range(self.num_players):
                # allow players to show information
                self.share_info_window()

                # allow each current player to play
                curr_player: 'Player' = self.players[curr_player_idx]

                played_card = self.play_card_window(curr_player)

                self.curr_trick[curr_player] = played_card

                if i == 0: # if start of the round, assign the trump_color color
                    self.trump_color = played_card.color

                curr_player_idx = (curr_player_idx + 1) % self.num_players

            # award one player the trick and set them to start the next round
            winner = self.check_trick_winner()
            self.start_player_idx = winner.id

            game_status = self.get_game_status()

            if game_status == 'lost':
                print('Lost game')

            elif game_status == 'done':
                print('Y\'all won! Go celebrate w boba')



    def get_game_status(self):

        completed_tasks = 0
        task: 'Task'
        for player, task in self.task_assignments:
            task.update_completion(self, player)
            if task.is_complete:
                completed_tasks += 1
            elif task.is_impossible:
                return 'lost'

        if completed_tasks == 2:
            return 'won'

        return 'ongoing'


        


        

        
