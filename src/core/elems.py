from abc import ABC
from copy import copy
import random

from src.core.card import Rank, Suit, Card

class Pile(ABC):
    def __init__(self):
        self.cards = []
    
    def addCard(self, card: Card) -> None:
        if isinstance(card, Card):
            self.cards.append(card)
        
    def getCard(self, index:int = 0) -> Card:
        if self.vol > 0:
            return self.cards.pop(index)
        else:
            return None

    # cards is being shifted from current pile into 'dest'
    # amount of cards to be moved, by default - all
    def shift(self, receiver, amount: int = None):
        if amount == None:
            amount = self.vol
        for _ in range(amount):
            receiver.addCard(self.getCard())

    def hideCards(self) -> None:
        self.cards = [None]*self.vol

    @property
    def vol(self) -> int:
        return len(self.cards)
    

class Deck(Pile):
    def __init__(self):
        super().__init__()
        for s in Suit:
            for r in Rank:
                c = Card(s, r)
                self.addCard(c)

    def shuffle(self):
        random.shuffle(self.cards)
            

class Stock(Pile):
    def __init__(self):
        super().__init__()
        self.__trump = None
        self.__last = None
    
    def setTrump(self) -> None:
        if self.vol > 0:
            first_card = self.getCard()
            self.__trump = first_card.suit
            # put first_card to the bottom
            self.addCard(first_card)
            self.__last = first_card
    
    def hideCards(self) -> None:
        last = self.last
        super().hideCards()
        if last:
            self.cards[-1] = last
    
    # non-empty Stock can show only last card
    @property
    def last(self) -> Card:
        if self.vol > 0:
            return self.__last
        else:
            return None
    
    @property
    def trump(self) -> Suit:
        return self.__trump


class Table(ABC):
    def __init__(self):
        self.top = Pile()
        self.low = Pile()
     
    def shift(self, receiver: Pile):
        self.top.shift(receiver)
        self.low.shift(receiver)
        
    def hasRank(self, r: Rank):
        piles = [self.top, self.low]
        for pile in piles:
            for card in pile.cards:
                if card.rank == r:
                    return True
        else:
            return False

    def showLastDown(self) -> Card:
        if self.low.vol > 0:
            return self.low.cards[-1]
        else:
            return None
    
