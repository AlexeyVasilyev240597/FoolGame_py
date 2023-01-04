from abc import ABC, abstractmethod
from items import Suit, Rank, Side, Card

import copy

class CardSet(ABC):
    def __init__(self, set_type):
        self._cards = set_type()
    
    @abstractmethod
    def addCard(self, card) -> None:
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


# testing block
# TODO: transfer this block to separate file with unit tests

def print_sets(s1: CardSet, s2: CardSet):
    print(f's1 = {s1}')
    print(f's2 = {s2}')
    
def test_open_sets(s1: CardSet, s2: CardSet):
    s1.shift(s2, True)
    print('\n test of shifting s1 -> s2 with opening s1')
    print_sets(s1, s2)

def test_close_sets(s1: CardSet, s2: CardSet):
    s2.shift(s1, True)
    print('\n test of shifting s2 -> s1 with closing s2')
    print_sets(s1, s2)
    for c in s1._cards:
        c.flip()
    print('and opening s1 for checking')
    print_sets(s1, s2)

s1 = CardSetNoGraphic()
s1.addCard(Card(Suit.DIAMONDS, Rank.SIX))
s1.addCard(Card(Suit.DIAMONDS, Rank.SEVEN))

s2 = CardSetNoGraphic()
s2.addCard(Card(Suit.HEARTS, Rank.EIGHT, Side.FACE))
s2.addCard(Card(Suit.HEARTS, Rank.NINE,  Side.FACE))

print_sets(s1, s2)

test_open_sets(copy.deepcopy(s1), copy.deepcopy(s2))

test_close_sets(copy.deepcopy(s1), copy.deepcopy(s2))

