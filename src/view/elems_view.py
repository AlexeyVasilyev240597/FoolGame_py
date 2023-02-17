from abc import ABC, abstractmethod

# from .card_view import CardView
from src.core.elems import Deck, Stock, Table


class DeckView(ABC):
    def __init__(self):
        ABC.__init__(self)
        self.vol = 0

    def update(self, deck: Deck):
        self.vol = deck.vol
    
    @abstractmethod
    def draw(self):
        pass


class StockView(ABC):
    def __init__(self):
        ABC.__init__(self)
        self.trump = None
        self.last  = None
        self.vol   = 0
    
    def update(self, stock: Stock):
        self.trump = stock.trump
        self.last  = stock.last
        self.vol   = stock.vol
    
    @abstractmethod
    def draw(self):
        pass


class TableView(ABC):
    def __init__(self):
        ABC.__init__(self)
        self.top = []
        self.low = []

    def update(self, table: Table):
        # self.top = [CardView(card) for card in table.top.cards]
        # self.low = [CardView(card) for card in table.low.cards]
        self.top = table.top.cards
        self.low = table.low.cards
    
    @abstractmethod
    def draw(self):
        pass
