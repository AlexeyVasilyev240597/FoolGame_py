import pygame
import random

from params import WIDTH, HEIGHT, CARD_W, CARD_H, BADGE_S, MAGIC_CONST
from items import Rank, Suit, CardS, TextBox, Badge, DECK_VOLUME

class Element:
    def __init__(self, pos):
        self.pos = pos
        self.cards = pygame.sprite.LayeredUpdates()
    
    def addCard(self, card, layer = 0, pos_loc = [0, 0]):        
        pos = self.loc2glob(pos_loc)
        card.setTargetPos(pos)
        self.cards.add(card)
        self.cards.change_layer(card, layer)

    def loc2glob(self, pos_loc):
        return [self.pos[0] + pos_loc[0], self.pos[1] + pos_loc[1]]

    def vol(self):
        return len(self.cards.sprites())

    def draw(self, screen):
        self.cards.draw(screen)
        
    def update(self):
        self.cards.update()

class Deck(Element):
    def __init__(self):
        Element.__init__(self, [0, 0])
        for s in Suit:
            for r in Rank:
                c = CardS(s, r)
                self.addCard(c, DECK_VOLUME-self.vol()-1)

    def shuffle(self):
        lrs = self.cards.layers()
        random.shuffle(lrs)
        for n in range(len(lrs)):
            self.cards.switch_layer(n, lrs[n])

    def getFromTop(self, by_open = False):
        c = self.cards.get_top_sprite()
        if by_open:
            c.flip()        
        self.cards.remove(c)
        return c

    def getFromBottom(self, by_open = False):        
        c = self.cards.get_sprite(0)
        if by_open:
            c.flip()
        self.cards.remove(c)
        return c

class Pile(Element):
    def __init__(self):
        Element.__init__(self, [WIDTH - CARD_W, HEIGHT/2 - CARD_H/2])
    

class Stock(Element):
    def __init__(self):
        Element.__init__(self, [0, HEIGHT/2 - CARD_H/2])
        self.trump_badge = pygame.sprite.Group()
        self.counter = []
    
    def showTrump(self):        
        last_card = self.cards.get_top_sprite()       
        last_card.flip()
        last_card.setTargetPos([self.pos[0], self.pos[1] + CARD_W/4])
        last_card.image = pygame.transform.rotate(last_card.image, -90)
        self.cards.move_to_back(last_card)
        # set info box params
        box_pos = self.loc2glob([CARD_W/2-BADGE_S/2, CARD_H/2-BADGE_S/2])
        box_size = [BADGE_S, BADGE_S]
        # init trump badge
        tb = Badge(last_card.suit, box_pos)  
        self.trump_badge.add(tb)
        # init counter
        self.counter = TextBox(box_pos, box_size)
        self.counter.setText(str(self.vol()))
        # self.info_box.add(self.counter)
        return last_card.suit
    
    def getCard(self, by_open = False):
        n = self.vol()
        if n > 0:
            card = self.cards.get_top_sprite()
            if n == 1:
                card.image = pygame.transform.rotate(card.image, 90)                
            else:
                card.flip()
            if not by_open:
                card.flip()
            self.cards.remove(card)
        else:
            card = []
        self.counter.setText(str(self.vol()))
        return card
        
    def draw(self, screen):
        self.cards.draw(screen)        
        if self.vol() > 1 and not self.counter == []:
            self.counter.draw(screen)
        if self.vol() == 0 and not self.counter == []:
            self.trump_badge.draw(screen)
        

class Table(Element):
    def __init__(self):
        Element.__init__(self, [WIDTH/2 - MAGIC_CONST*CARD_W/2, 13/8*CARD_H])
        print(self.pos)
        self.last_down = 0
        self.last_up   = 0
        
    def addCard(self, card, atop):
        if atop:
            l = 2*(self.last_up + 1)
            self.last_up += 1
        else:
            l = 2*self.last_down + 1
            self.last_down += 1
        
        pos = self.getCardPos(l)        
        Element.addCard(self, card, l, pos)
        
    def getCardPos(self, layer):
        i    = layer - 1
        atop = layer % 2
        x = (i %  MAGIC_CONST) * CARD_W        
        y = (i // MAGIC_CONST) * CARD_H
        if atop:
            x += CARD_W / 4
            y += CARD_H / 4
        pos = [x, y]
        return pos
        
    def getAllCards(self, cards_set, by_open = False):
        while self.vol() > 0:
            card = self.cards.get_top_sprite()
            if not by_open:
                card.flip()
            cards_set.addCard(card)
            self.cards.remove(card)
        self.last_down = 0
        self.last_up   = 0


class Dealer:       
    def deck2player(deck, player, by_open = False):
        for n in range(MAGIC_CONST):
            card = deck.getFromTop(by_open)
            player.addCard(card)
    
    def deck2stock(deck, stock):
        while len(deck.cards) > 0:
            card = deck.getFromBottom()
            # stock.addCard(card, stock.vol())
            stock.addCard(card)

    # call in start of Fool Game
    def deal(deck, players, stock):
        Dealer.deck2player(deck, players['active'],  True)
        Dealer.deck2player(deck, players['passive'], True)
        Dealer.deck2stock(deck, stock)
        
    # call in finish of Fool Game
    def pile2deck(pile, deck):
        while len(pile.sprites()) > 0:
            card = pile.get_top_sprite()
            deck.addCard(card)
            card.setTargetPos(deck.pos)
            pile.cards.remove(card)