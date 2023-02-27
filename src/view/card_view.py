from abc import ABC, abstractmethod

from src.core.card import Card, Side

class CardView(ABC, Card):
    def __init__(self, card: Card):
        ABC.__init__(self)
        if card.open:
            side = Side.FACE
        else:
            side = Side.BACK
        Card.__init__(self, card.suit, card.rank, side)
    
    @abstractmethod
    def cardView2card(card_view):
        pass
    
    @abstractmethod
    def draw(self):
        pass
