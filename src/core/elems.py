from abc import ABC
import random

from src.core.card import Rank, Suit, Card

class Pile(ABC):
    def __init__(self):
        self.cards = []
    
    def addCard(self, card: Card) -> None:
        if isinstance(card, Card):
            self.cards.append(card)
        
    def getCard(self, to_flip: bool = False, index: int = 0) -> Card:
        if self.vol > 0:
            card = self.cards.pop(index)
            if to_flip:
                card.flip()
            return card
        else:
            return None

    # swop of one card from current pile into 'receiver'
    # index is 0 by default (from top if it is simple pile)
    def swop(self, receiver, to_flip: bool = False, index: int = 0) -> None:
        receiver.addCard(self.getCard(to_flip, index))

    # cards are being shifted from current pile into 'receiver'
    # amount of cards to be moved, all by default
    def shift(self, receiver, to_flip: bool = False, amount: int = None):
        if amount == None:
            amount = self.vol
        for _ in range(amount):
            self.swop(receiver, to_flip)

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
    
    def getCard(self, to_flip: bool = False, index: int = 0) -> Card:
        # last card is open
        if self.vol == 1:
            to_flip = not to_flip
        return super().getCard(to_flip, index)
    
    def setTrump(self) -> None:
        if self.vol > 0:
            first_card = self.getCard(to_flip=True)
            self._trump = first_card.suit
            # put first_card to the bottom
            self.addCard(first_card)
            self._last = first_card
    
    # def hideCards(self) -> None:
    #     last = self.last
    #     super().hideCards()
    #     if last:
    #         self.cards[-1] = last
    
    # non-empty Stock can show only last card
    @property
    def last(self) -> Card:
        if self.vol > 0:
            return self._last
        else:
            return None
    
    @property
    def trump(self) -> Suit:
        return self._trump


class Table(ABC):
    def __init__(self):
        self.top = Pile()
        self.low = Pile()
     
    def shift(self, receiver: Pile, to_flip: bool = False):
        self.top.shift(receiver, to_flip)
        self.low.shift(receiver, to_flip)
        
    def hasRank(self, r: Rank) -> bool:
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
    
