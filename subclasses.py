from typing import List
from copy import deepcopy

class Player:

    def __init__(self, is_agent: bool, id: int) -> None:
        self.is_agent = is_agent
        self.cards_in_hand = []
        self.starting_hand = []
        self.id = id

        self.cards_won = []
        self.tricks_won = 0

        self.token_position = 'unused' # token_positions -> 'unused', 'used', 'lowest', 'only', 'highest'
        self.revealed_card = None
        self.task = None

    def assign_hand(self, hand: List['Card']) -> None:
        self.starting_hand = deepcopy(hand)
        self.cards_in_hand = deepcopy(hand)

    def get_printable_hand(self) -> List[str]:
        printable_hand = []

        card: 'Card'
        for card in self.cards_in_hand:
            printable_hand.append(str(card))

        return printable_hand

    def share_info(self, sharing_card: 'Card', position: str) -> bool:
        """
        Makes sure that sharing the input card and position is correct and valid
        If so, it performs the info sharing
        """

        # Make sure player has this card or that it's not a SUB card (can't share info on subs)
        if sharing_card not in self.cards_in_hand or sharing_card.color == 'SUB':
            return False

        # Check conditions based on position of information sharing
        if position == 'lowest':
            # If there is another card of this color with lower number, indicate invalid information share
            for card in self.cards_in_hand:
                if card != sharing_card and card.color == sharing_card.color and card.number < sharing_card.number:
                    return False
        elif position == 'only':
            # If there is another card of this color, indicate invalid information share
            for card in self.cards_in_hand:
                if card != sharing_card and card.color == sharing_card.color:
                    return False
        elif position == 'highest':
            # If there is a card of this color with higher number, indicate invalid information share
            for card in self.cards_in_hand:
                if card != sharing_card and card.color == sharing_card.color and card.number > sharing_card.number:
                    return False
        else:
            # If invalid position name, indicate invalid information share
            return False

        # Set the revealed card
        self.revealed_card = deepcopy(card)
        self.token_position = position
        return True

    def play_card(self, card: 'Card') -> 'Card':
        if card == self.revealed_card:
            self.revealed_card = None
            self.token_position = 'used'
        played_card = self.cards_in_hand.pop(self.cards_in_hand.index(card))
        return played_card

class Card:

    def __init__(self, color: str, number: int) -> None:
        self.color = color
        self.number = number

    def __eq__(self, otherCard: 'Card') -> bool:
        return self.color == otherCard.color and self.number == otherCard.number

    def __str__(self) -> str:
        return self.color + "_" + str(self.number)
            
class Task:

    def __init__(self, name: str) -> None:
        self.name = name
        self.is_complete = False
        self.is_impossible = False
    
    def update_completion(self, game, owner: 'Player') -> None:
        """
        This function takes in the player info and checks if the task is complete
        """
        is_complete = False
        is_impossible = False
        remaining_rounds = game.total_rounds - game.num_rounds_complete

        if self.name == 'less_than_captain':
            # If there is no way for owner to win >= tricks as captain, task is complete
            if game.captain.tricks_won > remaining_rounds + owner.tricks_won:
                is_complete = True
            # If there's no way for captain to have > tricks as owner, task is impossible
            elif game.captain.tricks_won + remaining_rounds <= owner.tricks_won:
                is_impossible = True
        elif self.name == 'no_green_no_yellow':
            # If owner has won a green or yellow card the task is impossible to complete
            for card in owner.cards_won:
                if card.color == 'green' or card.color == 'yellow':
                    is_impossible = True
                    break
            # If there are no more rounds and player hasn't won a green/yellow then task is complete
            if remaining_rounds == 0 and not is_impossible:
                is_complete = True
        elif self.name == 'exactly_2_tricks':
            # If player has won more than 2 tricks or not enough rounds left to win 2, task is impossible
            if remaining_rounds + owner.tricks_won < 2 or owner.tricks_won > 2:
                is_impossible = True
            # If there are no more rounds and player has won exactly two tricks then task is complete
            elif remaining_rounds == 0 and owner.tricks_won == 2:
                is_complete = True
        elif self.name == 'win_using_a_6':
            # If player has won a trick using a 6, task is complete
            for card in owner.cards_won:
                if card.number == 6 and card in owner.starting_hand:
                    is_complete = True
            # If player hasn't completed task and doesn't have any more 6's then task is impossible
            if not is_complete:
                is_impossible = True
                for card in owner.cards_in_hand:
                    if card.number == 6:
                        is_impossible = False
                        break
        elif self.name == 'win_green5_blue8':
            # If player has won the green5 and blue8 then task is complete
            found_green_5, found_blue_8 = False, False
            for card in owner.cards_won:
                if card == Card('green', 5):
                    found_green_5 = True
                elif card == Card('blue', 8):
                    found_blue_8 = True
            if found_green_5 and found_blue_8:
                is_complete = True
                
        # Set the Task's variables
        self.is_complete = is_complete
        self.is_impossible = is_impossible


