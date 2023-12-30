from abc import ABC, abstractmethod

from src.core.card import Side, Card
from src.core.elems import Pile, Deck, Stock, Table


class ItemView(ABC):
    def __init__(self):
        ABC.__init__(self)
    
    @abstractmethod
    def card2cardView(card: Card):
        pass
    
    @abstractmethod
    def draw(self):
        pass
  
    # @abstractmethod
    # def update(self, pile: Pile):
    #     pass

class PileView(Pile, ItemView):
    def __init__(self):
        Pile.__init__(self)
        ItemView.__init__(self)

class DeckView(Deck, ItemView):
    def __init__(self):
        Deck.__init__(self)
        ItemView.__init__(self)
        [card.hide() for card in self.cards]
        for i in range(len(self.cards)):
            self.cards[i] = self.card2cardView(self.cards[i])
        
class StockView(Stock, ItemView):
    def __init__(self):
        Stock.__init__(self)
        ItemView.__init__(self)
    

# maybe you don't need dublate the constructor
# TODO: check it!
class TableView(Table, ItemView):
    def __init__(self):
        Table.__init__(self)
        ItemView.__init__(self)
