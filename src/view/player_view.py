from abc import ABC, abstractmethod

# from .card_view import CardView
from src.view.elems_view import ItemView
from src.view.card_convert import CardConverter
from src.core.player import Player


class PlayerView(Player, ItemView):
    def __init__(self, is_graphic):
        Player.__init__(self)
        ItemView.__init__(self, is_graphic)
    
    # def update(self, player: Player):
    #     self.status = player.status
    #     # game params
    #     self.trump  = player.trump
    #     self.cards  = [CardConverter.card2cardView(card, self.is_graphic) for card in player.cards]
    
    
class PlayerSbjView(ItemView):
    def __init__(self, is_graphic: bool, name: str, id: int) -> None:
        ItemView.__init__(self, is_graphic)
        self.name   = name
        self.id = id
        self.word = None
        self.is_active = False
    
    def update(self, last_move: dict, actv_id: int):        
        if ('pl_id' in last_move and 
            self.id == last_move['pl_id'] and
            'word' in last_move):
            self.word = last_move['word']
        else:
            self.word = None
        self.is_active = self.id == actv_id
    