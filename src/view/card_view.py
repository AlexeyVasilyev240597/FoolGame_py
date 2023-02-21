from abc import ABC, abstractmethod

from src.core.card import Card

class CardView(ABC, Card):
    def __init__(self, card: Card):
        ABC.__init__(self)
        if card.open:
            Card.__init__(self, card.suit, card.rank)
        else:
            Card.__init__(self)
    
    @abstractmethod
    def cardView2card(card_view):
        pass
    
    @abstractmethod
    def draw(self):
        pass
