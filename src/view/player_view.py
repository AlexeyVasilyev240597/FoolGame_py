from abc import ABC, abstractmethod

# from .card_view import CardView
from src.core.player import Player

class PlayerView(ABC):
    def __init__(self, player: Player):
        ABC.__init__(self)
        self.name   = player.name
        self.status = player.status
        # game params
        self.trump  = player.trump
        # self.cards  = [CardView(card) for card in player.cards]
        self.cards  = player.cards

    @abstractmethod
    def draw(self):
        pass
