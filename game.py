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

        # initialize players
        for i in range(self.num_players):
            if i < self.num_bots:
                player = Player(is_agent = True)
            else:
                player = Player(is_agent = False)
            
            self.players.append(player)


        # initialize tasks (sample 2 from the 5 total)

        self.tasks = np.random.choice(list(range(self.num_unique_tasks)), size = 2, replace = False)

        self.tasks = [Task(i) for i in self.tasks]


        
    def initialize(self):
        # assign hands, sample tasks

    def play(self):


    def is_game_over(self):

        for player, task in self.task_assignments:
            if not task.is_complete(player):
                return False

        return True


        


        

        
