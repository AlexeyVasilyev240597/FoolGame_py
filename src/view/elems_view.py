from abc import ABC, abstractmethod

from src.view.card_convert import CardConverter
from src.core.elems import Pile, Deck, Stock, Table


class PileView(ABC):
    def __init__(self, is_graphic: bool):
        ABC.__init__(self)
        self.is_graphic = is_graphic
    
    @abstractmethod
    def draw(self):
        pass
  
    @abstractmethod
    def update(self, pile: Pile):
        pass

class DeckView(PileView):
    def __init__(self, is_graphic: bool):
        PileView.__init__(self)
        self.vol = 0

    def update(self, deck: Deck):
        self.vol = deck.vol
    

class StockView(PileView):
    def __init__(self, is_graphic: bool):
        PileView.__init__(self)
        self.trump = None
        self.last  = None
        self.vol   = 0
    
    def update(self, stock: Stock):
        self.trump = stock.trump
        self.last  = stock.last
        self.vol   = stock.vol
    

class TableView(PileView):
    def __init__(self, is_graphic: bool):
        PileView.__init__(self)
        self.top = []
        self.low = []

    def update(self, table: Table):
        # for card_view in self.top.cards:
        #     if not card
        self.top = [CardConverter.card2cardView(card, self.is_graphic) for card in table.top.cards]
        self.low = [CardConverter.card2cardView(card, self.is_graphic) for card in table.low.cards]
        # self.top = table.top.cards
        # self.low = table.low.cards
    
