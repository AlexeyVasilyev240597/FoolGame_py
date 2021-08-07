import random

from params import MAGIC_CONST, FLAG_DEBUG
from items import Rank, Suit, Card

class Pile:
    def __init__(self):
        self.cards = []
    
    def addCard(self, card):
        self.cards.append(card)
        
    def getCard(self, to_flip = False, index = 0):        
        c = self.cards.pop(index)
        if to_flip:
            c.flip()
        return c

    def shift(self, pile, to_flip = False):
        while self.vol() > 0:
            pile.addCard(self.getCard(to_flip))

    def vol(self):
        return len(self.cards)

class Deck(Pile):
    def __init__(self):
        Pile.__init__(self)
        for s in Suit:
            for r in Rank:
                c = Card(s, r)
                # DEBUG
                # c.flip()
                self.addCard(c)

    def shuffle(self):
        random.shuffle(self.cards)
            

class Stock(Pile):
    def showTrump(self):
        last_card = self.getCard(True)
        self.addCard(last_card)
        self.trump = last_card.suit
        return self.trump
    
    def getCard(self, by_open = False):
        n = self.vol()
        card = Pile.getCard(self, by_open)
        if n == 1:
            card.flip()
        return card

class Table(Pile):
    def __init__(self):
        Pile.__init__(self)
        self.cards = {'up': [], 'down': []}

    def addCard(self, card, atop):
        if atop:
            self.cards['up'].append(card)
        else:
            self.cards['down'].append(card)
     
    def shift(self, pile, to_flip = False):
        self.cards = self.cards['up'] + self.cards['down']
        Pile.shift(self, pile, to_flip)
        self.cards = {'up': [], 'down': []}
    
    def vol(self, key = 'all'):
        if key == 'all':
            if 'up' in self.cards and 'down' in self.cards:
                return len(self.cards['up'] + self.cards['down'])
            else:
                return len(self.cards)
        else:
            return len(self.cards[key])

class Dealer: 
    def deck2player(deck, player, by_open = False):
        for n in range(MAGIC_CONST):
            card = deck.getCard(by_open, 0)
            player.addCard(card)
    
    # call in start of Fool Game
    def deal(deck, players, stock):
        Dealer.deck2player(deck, players['pssv'], FLAG_DEBUG or players['pssv'].is_user)
        Dealer.deck2player(deck, players['actv'], FLAG_DEBUG or players['actv'].is_user)
        deck.shift(stock)
        trump = stock.showTrump()
        players['actv'].setTrump(trump)
        players['pssv'].setTrump(trump)
        return trump
    
    # call in finish of Fool Game
    def all2deck(players, table, pile, deck):
        for role in players:
            while players[role].vol() > 0:
                deck.addCard(players[role].getCard())
        table.shift(deck, True)
        pile.shift(deck)