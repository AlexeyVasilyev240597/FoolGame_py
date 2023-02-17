from abc import ABC, abstractmethod

# from .card_view import CardView
from src.core.player import Player


class PlayerView(ABC):
    def __init__(self):
        ABC.__init__(self)
        self.status = None
        # game params
        self.trump  = None
        self.cards  = []
        # self.mes_box = None

    def update(self, player: Player):
        self.status = player.status
        # game params
        self.trump  = player.trump
        # self.cards  = [CardView(card) for card in player.cards]
        self.cards  = player.cards
    
    @abstractmethod
    def draw(self):
        pass


# class PlayersView(ABC):
#     def __init__(self, pl_1_v: PlayerView, pl_2_v: PlayerView):
#         ABC.__init__(self)
#         self.rival = pl_1_v
#         self.me = pl_2_v
    
    
class PlayerSbjView(ABC):
    def __init__(self, name: str, id: int) -> None:
        ABC.__init__(self)
        self.name   = name
        self.id = id
        self.word = None
        self.is_active = False
    
    def update(self, last_move: dict, is_active: bool):
        if ('pl_id' in last_move and 
            self.id == last_move['pl_id'] and
            'word' in last_move):
            self.word = last_move['word']
        else:
            self.word = None
        self.is_active = is_active
    
    @abstractmethod
    def draw(self):
        pass
