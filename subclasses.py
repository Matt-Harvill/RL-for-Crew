from typing import List 

# token_positions -> 'unused', 'used', 'lowest', 'only', 'highest'

class Player:

    def __init__(self, is_agent: bool) -> None:
        self.is_agent = is_agent
        self.hand = []
        self.token_position = 'unused'
        self.revealed_card = None
        self.task = None

    def assign_hand(self, hand: List['Card']) -> None:
        self.hand = hand

    def share_info(self, card: 'Card', position: str) -> None:
        self.revealed_card = card
        self.token_position = position

    def play_card(self, card: 'Card') -> 'Card':
        if card == self.revealed_card:
            self.revealed_card = None
            self.token_position = 'used'
        played_card = self.hand.pop(self.hand.index(card))
        return played_card

class Card:

    def __init__(self, color: str, number: int) -> None:
        self.color = color
        self.number = number

    def __eq__(self, otherCard: 'Card') -> bool:
        return self.color == otherCard.color and self.number == otherCard.number
            
class Task:

    def __init__(self, task_id: int) -> None:
        self.id = task_id
        self.is_complete = False

    def complete_task(self) -> None:
        self.is_complete = True


