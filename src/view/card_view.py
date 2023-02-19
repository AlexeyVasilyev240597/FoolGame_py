from abc import ABC, abstractmethod

from src.core.card import Card

class CardView(ABC, Card):
    def __init__(self, card: Card = None):
        ABC.__init__(self)
        # if 'card' argument is None it means the card is face down
        if card:
            Card.__init__(self, card.suit, card.rank)
            self.open = True
        else:
            Card.__init__(self, None, None)
            self.open = False
    
    @abstractmethod
    def cardView2card(card_view):
        pass
    
    @abstractmethod
    def draw(self):
        pass
