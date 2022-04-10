import pygame
import random

from params import CARD_W, CARD_H, BADGE_S, MAGIC_CONST, FLAG_DEBUG
from params import POS_STOCK, POS_PILE, POS_TABLE
from items import Rank, Suit, CardS, TextBox, Badge, DECK_VOLUME

class Element:
    def __init__(self, pos):
        self.pos = pos
        self._cards = pygame.sprite.LayeredUpdates()
    
    def addCard(self, card, layer = 0, pos_loc = [0, 0]):
        pos = self.loc2glob(pos_loc)
        card.setTargetPos(pos)
        self._cards.add(card)
        self._cards.change_layer(card, layer)
        
    def getCard(self, to_flip = False, index = -1):        
        c = self._cards.sprites()[index]
        if to_flip:
            c.flip()
        self._cards.remove(c)
        return c
    
    def showCard(self, indx):
        if indx < self.vol():
            return self._cards.sprites()[indx]

    def loc2glob(self, pos_loc):
        return [self.pos[0] + pos_loc[0], self.pos[1] + pos_loc[1]]

    def vol(self):
        return len(self._cards.sprites())

    def draw(self, screen):
        self._cards.draw(screen)
        
    def update(self):
        self._cards.update()

class Deck(Element):
    def __init__(self):
        Element.__init__(self, [0, 0])
        for s in Suit:
            for r in Rank:
                c = CardS(s, r)
                self.addCard(c)

    def addCard(self, card):
        Element.addCard(self, card, DECK_VOLUME-self.vol()-1)

    def shuffle(self):
        lrs = self._cards.layers()
        random.shuffle(lrs)
        for n in range(len(lrs)):
            self._cards.switch_layer(n, lrs[n])

class Pile(Element):
    def __init__(self):
        Element.__init__(self, POS_PILE)
        
    def showCard(self, indx):
        pass
    

class Stock(Element):
    def __init__(self):
        Element.__init__(self, POS_STOCK)
        self.trump_badge = pygame.sprite.Group()
        self.counter = []
    
    def showTrump(self):
        last_card = self._cards.get_top_sprite()
        last_card.flip()
        last_card.setTargetPos([self.pos[0], self.pos[1] + CARD_W/4])
        last_card.image = pygame.transform.rotate(last_card.image, -90)
        self._cards.move_to_back(last_card)
        # set info box params
        box_pos = self.loc2glob([CARD_W/2-BADGE_S/2, CARD_H/2-BADGE_S/2])
        box_size = [BADGE_S, BADGE_S]
        # init trump badge
        tb = Badge(last_card.suit, box_pos)  
        self.trump_badge.add(tb)
        # init counter
        self.counter = TextBox(box_pos, box_size)
        self.counter.setText(str(self.vol()))
        return last_card.suit
    
    def getCard(self, by_open = False):
        n = self.vol()
        card = Element.getCard(self, by_open)
        if n == 1:
            card.image = pygame.transform.rotate(card.image, 90)  
            card.flip()
        self.counter.setText(str(self.vol()))
        return card
    
    def showCard(self, indx):
        if self.vol() > 0 and indx == self.vol() - 1:
            return self._cards.sprites()[indx]        

    def draw(self, screen):
        self._cards.draw(screen)        
        if self.vol() > 1 and not self.counter == []:
            self.counter.draw(screen)
        if self.vol() == 0 and not self.counter == []:
            self.trump_badge.draw(screen)
        

class Table(Element):
    def __init__(self):
        Element.__init__(self, POS_TABLE)
        self._cards = {'up':   pygame.sprite.LayeredUpdates(),
                      'down': pygame.sprite.LayeredUpdates()}
        
    def addCard(self, card, atop):
        if atop:
            self._cards['up'].add(card)
            self._cards['up'].change_layer(card, 1)
            pos_loc = self.getCardPos('up')
        else:
            self._cards['down'].add(card)
            self._cards['down'].change_layer(card, 0)
            pos_loc = self.getCardPos('down')
            
        pos = self.loc2glob(pos_loc)
        card.setTargetPos(pos)        
        
    def getCardPos(self, layer):
        i = self.vol(layer) - 1
        # 6 / 2 = 3 in row for each layer
        if layer == 'down':
            n = 2 * (i % (MAGIC_CONST // 2))
        else: #if layer == 'up':
            n = 2 * (i % (MAGIC_CONST // 2)) + 1
        x = n * CARD_W   
        # 6 / 3 = 2 in col for each layer
        y = (i // (MAGIC_CONST // 2)) * CARD_H
        if layer == 'down':
            x += CARD_W / 4
            y += CARD_H / 4
        pos = [x, y]
        return pos
        
    def getAllCards(self, cards_set, by_open = False):
        for layer in self._cards:
            while self.vol(layer) > 0:
                card = self._cards[layer].sprites()[0]
                if not by_open:
                    card.flip()
                self._cards[layer].remove(card)
                cards_set.addCard(card)
        
    def showCard(self, layer, indx):
        if indx < self.vol(layer):
            return self._cards[layer].sprites()[indx]
        
    def vol(self, layer = 'both'):
        if layer == 'both':
            if 'up' in self._cards and 'down' in self._cards:
                return len(self._cards['up']) + len(self._cards['down'])
            else:
                return len(self._cards)
        else:
            return len(self._cards[layer])

    def draw(self, screen):
        self._cards['down'].draw(screen)
        self._cards['up'].draw(screen)
        
    def update(self):
        self._cards['down'].update()
        self._cards['up'].update()

class Dealer: 
    def deck2player(deck, player, by_open = False):
        for n in range(MAGIC_CONST):
            card = deck.getCard(by_open, 0)
            player.addCard(card)
    
    def deck2stock(deck, stock):
        while deck.vol() > 0:
            card = deck.getCard(False, 0)
            stock.addCard(card)

    # call in start of Fool Game
    def deal(deck, pl1, pl2, stock):
        if FLAG_DEBUG:
            Dealer.deck2player(deck, pl1, True)
            Dealer.deck2player(deck, pl2,  True)
        else:
            Dealer.deck2player(deck, pl2, pl2.is_user)
            Dealer.deck2player(deck, pl1,  pl1.is_user)
        Dealer.deck2stock(deck, stock)
        trump = stock.showTrump()
        return trump
    
    # call in finish of Fool Game
    def all2deck(players, table, pile, deck):
        for pl in players:
            while pl.vol() > 0:
                card = pl.getCard()
                deck.addCard(card)
        table.getAllCards(deck)
        while pile.vol() > 0:
            card = pile.getCard()
            deck.addCard(card)
