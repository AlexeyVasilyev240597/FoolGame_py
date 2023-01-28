from abc import ABC
from copy import copy
import random

from card import Rank, Suit, Card

class Pile(ABC):
    def __init__(self):
        self.__cards = []
    
    def addCard(self, card: Card) -> None:
        self.__cards.append(card)
        
    def getCard(self, index:int = 0) -> Card:
        if self.vol() > 0:
            return self.__cards.pop(index)
        else:
            return None

    # cards is being shifted from current pile into 'dest'
    # amount of cards to be moved, by default - all
    def shift(self, dest, amount: int = None):
        if amount == None:
            amount = self.vol
        for _ in range(amount):
            dest.addCard(self.getCard())

    def hideCards(self) -> None:
        self.__cards = [None]*self.vol

    @property
    def vol(self):
        return len(self.__cards)


class Deck(Pile):
    def __init__(self):
        super().__init__()
        for s in Suit:
            for r in Rank:
                c = Card(s, r)
                self.addCard(c)

    def shuffle(self):
        random.shuffle(self.__cards)
            

class Stock(Pile):
    def __init__(self):
        super().__init__()
        self.__trump = None
        self.__last = None
    
    def setTrump(self) -> Suit:
        if self.vol() > 0:
            first_card = self.getCard()
            self.__trump = first_card.suit
            # put first_card to the bottom
            self.addCard(first_card)
            self.__last = first_card
        return self.trump
    
    def hideCards(self) -> None:
        last = self.last
        super().hideCards()
        self.__cards[-1] = last
    
    # non-empty Stock can show only last card
    @property
    def last(self) -> Card:
        if self.vol() > 0:
            return self.__last
        else:
            return None
    
    @property
    def trump(self) -> Suit:
        return self.__trump


class Table(Pile):
    def __init__(self):
        self.__cards = {'up': [], 'down': []}

    def addCard(self, card: Card, atop: bool):
        if atop:
            self.__cards['up'].append(card)
        else:
            self.__cards['down'].append(card)
     
    def shift(self, pile):
        self.__cards = self.__cards['up'] + self.__cards['down']
        super().shift(self, pile)
        self.__cards = {'up': [], 'down': []}
    
    # by default: sum of volumes of down and up piles
    def vol(self, key = None):
        if key == None:
            return len(self.__cards['up'] + self.__cards['down'])
        elif key == 'down' or key == 'up':
            return len(self.__cards[key])
        else:
            return None            
    
    def hasRank(self, r: Rank):
        for layer in self.__cards:
            for card in self.__cards[layer]:
                if card.rank == r:
                    return True
        else:
            return False

    def showLastDown(self) -> Card:
        if self.vol() > 0:
            return self.__cards['down'][-1]
        else:
            return None
    
    def hideCards(self) -> None:
        pass
    
    @property
    def cards(self):
        return copy(self.__cards)
