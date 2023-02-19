from abc import ABC, abstractmethod

# from .card_view import CardView
from src.view.elems_view import PileView
from src.view.card_convert import CardConverter
from src.core.player import Player


class PlayerView(PileView):
    def __init__(self, is_graphic):
        PileView.__init__(self, is_graphic)
        self.status = None
        # game params
        self.trump  = None
        self.cards  = []
        # self.mes_box = None

    def update(self, player: Player):
        self.status = player.status
        # game params
        self.trump  = player.trump
        self.cards  = [CardConverter.card2cardView(card, self.is_graphic) for card in player.cards]
    
    
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
