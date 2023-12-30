from abc import ABC

from src.core.card import Side, Card

class CardView(ABC, Card):
    def __init__(self, card: Card):
        ABC.__init__(self)
        if card.open:
            side = Side.FACE
        else:
            side = Side.BACK
        Card.__init__(self, card.suit, card.rank, side)
    
    # virtual method
    def draw(self):
        return self.__repr__()
