from abc import ABC, abstractmethod
import random

from card import Card, Suit, Rank

class CardSet(ABC):
    def __init__(self, set_type):
        self._cards = set_type()
    
    @abstractmethod
    def addCard(self, card: Card) -> None:
        pass
    
    @abstractmethod
    def getCard(self, to_flip: bool = False, index: int = 0):
        pass
    
    @abstractmethod
    def showCard(self, index: int):
        pass
    
    @abstractmethod
    # cards from current set is being shifted into 'dest' set
    def shift(self, dest, to_flip: bool = False) -> None:
        pass
    
    @abstractmethod
    def vol(self) -> int:
        pass


# class Deck(CardSet):
#     def __init__(self, set_type):
#         super().__init__(set_type)
#         for s in Suit:
#             for r in Rank:
#                 c = Card(s, r)
#                 self.addCard(c)

#     def shuffle(self):
#         random.shuffle(self._cards)


class Stock(CardSet):
    def __init__(self, set_type):
        super().__init__(set_type)
        self.trump = None

    def setTrump(self):
        last_card = self.getCard(True)
        self.addCard(last_card)
        self.trump = last_card.suit
        return self.trump

class CardSetNoGraphic(CardSet):
    def __init__(self):
        super().__init__(list)
    
    def addCard(self, card: Card):
        self._cards.append(card)
        
    def getCard(self, to_flip = False, index = 0) -> Card:       
        c = self._cards.pop(index)
        if to_flip:
            c.flip()
        return c

    def showCard(self, indx):
        if indx < self.vol():
            return self._cards[indx]
    
    def shift(self, dest, to_flip: bool = False) -> None:
        while self.vol() > 0:
            dest.addCard(self.getCard(to_flip))  

    
    def vol(self):
        return len(self._cards)
    
    def __repr__(self):
        return self._cards.__repr__()

