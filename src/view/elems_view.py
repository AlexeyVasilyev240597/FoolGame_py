from abc import ABC, abstractmethod

from src.core.card import Side, Card
from src.view.card_convert import CardConverter
from src.core.elems import Pile, Deck, Stock, Table


class ItemView(ABC):
    def __init__(self, is_graphic: bool):
        ABC.__init__(self)
        self.is_graphic = is_graphic
    
    @abstractmethod
    def draw(self):
        pass
  
    # @abstractmethod
    # def update(self, pile: Pile):
    #     pass

class DeckView(Deck, ItemView):
    def __init__(self, is_graphic: bool):
        Deck.__init__(self)
        ItemView.__init__(self, is_graphic)
        [card.flip() for card in self.cards]
        for i in range(len(self.cards)):
            self.cards[i] = CardConverter.card2cardView(self.cards[i], self.is_graphic)
        [card.flip() for card in self.cards]
    
    def syncDeck(self, deck: Deck):
        [card.flip() for card in self.cards]
        [card.flip() for card in deck.cards]
        for i in range(len(self.cards)):
            card = Card(self.cards[i].suit, self.cards[i].rank, Side.FACE)
            j = deck.cards.index(card)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        # for c, c_v in zip(deck.cards, self.cards):
        #         print(f'deck: {c.rank}-{c.suit}, deck_view: {c_v.rank}-{c_v.suit}')
        [card.flip() for card in self.cards]
        [card.flip() for card in deck.cards]
        # NOTE: you need to pass deepcopy of deck 
        # (for don't changing cards in original deck)
        # or need to call card.flip for stay deck closed!

    # def update(self, deck: Deck):
    #     self.vol = deck.vol
    

class StockView(Stock, ItemView):
    def __init__(self, is_graphic: bool):
        Stock.__init__(self)
        ItemView.__init__(self, is_graphic)
        
    
    # def update(self, stock: Stock):
    #     self.trump = stock.trump
    #     if stock.last:
    #         self.last  = CardConverter.card2cardView(stock.last, self.is_graphic)
    #     else:
    #         self.last = None
    #     self.vol   = stock.vol
    

# maybe you don't need dublate the constructor
# TODO: check it!
class TableView(Table, ItemView):
    def __init__(self, is_graphic: bool):
        Table.__init__(self)
        ItemView.__init__(self, is_graphic)

    # def update(self, table: Table):
    #     self.top = [CardConverter.card2cardView(card, self.is_graphic) for card in table.top.cards]
    #     self.low = [CardConverter.card2cardView(card, self.is_graphic) for card in table.low.cards]
    
