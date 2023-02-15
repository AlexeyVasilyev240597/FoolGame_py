from abc import ABC, abstractmethod

# from .card_view import CardView
from src.core.elems import Deck, Stock, Table


class DeckView(ABC):
    def __init__(self, deck: Deck):
        ABC.__init__(self)
        self.vol = deck.vol
    
    @abstractmethod
    def draw(self):
        pass


class StockView(ABC):
    def __init__(self, stock: Stock):
        ABC.__init__(self)
        self.trump = stock.trump
        self.last  = stock.last
        self.vol   = stock.vol
    
    @abstractmethod
    def draw(self):
        pass


class TableView(ABC):
    def __init__(self, table: Table):
        ABC.__init__(self)
        # self.top = [CardView(card) for card in table.top.cards]
        # self.low = [CardView(card) for card in table.low.cards]
        self.top = table.top.cards
        self.low = table.low.cards
    
    @abstractmethod
    def draw(self):
        pass
