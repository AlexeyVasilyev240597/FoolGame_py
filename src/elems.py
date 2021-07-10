import pygame
import random

from params import WIDTH, HEIGHT, CARD_W, CARD_H, BADGE_S, MAGIC_CONST
from items import Rank, Suit, CardS, TextBox, Badge

class Element(pygame.sprite.LayeredUpdates):
    def __init__(self, pos):
        pygame.sprite.LayeredUpdates.__init__(self)
        self.pos = pos
        self.cards = []
    
    def addCard(self, card):
        self.cards.append(card)
        self.add(card)        
        card.setTargetPos(self.pos)
        self.change_layer(card, self.vol())

    def loc2glob(self, pos_loc):
        return [self.pos[0] + pos_loc[0], self.pos[1] + pos_loc[1]]

    def vol(self):
        return len(self.cards)

    def draw(self, screen):
        pygame.sprite.LayeredUpdates.draw(self, screen)

class Deck(Element):
    def __init__(self):
        Element.__init__(self, [0, 0])
        for s in Suit:
            for r in Rank:
                c = CardS(s, r)
                self.addCard(c)

    def shuffle(self):
        random.shuffle(self.cards)

    def getFromTop(self, by_open = False):
        c = self.cards.pop(0)
        if by_open:
            c.flip()
        #self.remove(c)
        return c

    def getFromBottom(self, by_open = False):
        c = self.cards.pop()
        if by_open:
            c.flip()
        #self.remove(c)
        return c

class Pile(Element):
    def __init__(self):
        Element.__init__(self, [WIDTH - CARD_W, HEIGHT/2 - CARD_H/2])
    

class Stock(Element):
    def __init__(self):
        Element.__init__(self, [0, HEIGHT/2 - CARD_H/2])
        self.trump_badge = []     
        self.counter = []
    
    def showTrump(self):        
        last_card = self.get_top_sprite()       
        last_card.flip()
        # print(last_card)
        last_card.setTargetPos([self.pos[0], self.pos[1] + CARD_W/4])
        last_card.image = pygame.transform.rotate(last_card.image, -90)
        self.change_layer(last_card, 0)
        
        box_pos = self.loc2glob([CARD_W/2-BADGE_S/2, CARD_H/2-BADGE_S/2])
        box_size = [BADGE_S, BADGE_S]
        self.trump_badge = Badge(last_card.suit, box_pos)        
        self.add(self.trump_badge)    
        self.move_to_back(self.trump_badge)   
        
        self.counter = TextBox(box_pos, box_size)
        self.counter.setText(str(self.vol()))
        # self.add(self.counter)
        # self.move_to_front(self.counter)
        
        return last_card.suit
    
    def getCard(self, by_open = False):
        n = self.vol()
        if n > 0:
            card = self.get_top_sprite()
            if n == 1:
                card.image = pygame.transform.rotate(card.image, 90)                
            else:
                card.flip()
            if not by_open:
                card.flip()
            self.remove(card)
            self.cards.remove(card)
        else:
            card = []
        self.counter.setText(str(self.vol()))
        
        return card
        
    def draw(self, screen):
        pygame.sprite.LayeredUpdates.draw(self, screen)
        if self.vol() > 1 and not self.counter == []:
            self.counter.draw(screen)

class Table(Element):
    def __init__(self):
        Element.__init__(self, [WIDTH/2 -  MAGIC_CONST*CARD_W/2, 13/8*CARD_H])
        self.last_down = 0
        self.last_up   = 0
        
    def addCard(self, card, atop):
        if atop:
            l = 2*(self.last_up + 1)
            self.last_up += 1
        else:
            l = 2*self.last_down + 1
            self.last_down += 1
        
        self.add(card, layer = l)
        self.cards.append(card)
        pos = self.getCardPos(l)
        card.setTargetPos(pos)
        
    def getCardPos(self, layer):
        i    = layer - 1
        atop = layer % 2
        x = (i %  MAGIC_CONST) * CARD_W        
        y = (i // MAGIC_CONST) * CARD_H
        if atop:
            x += CARD_W / 4
            y += CARD_H / 4
        x += self.pos[0]
        y += self.pos[1]
        pos = [x, y]
        return pos
        
    def getAllCards(self, cards_set, by_open = False):
        print(self.vol())
        while self.vol() > 0:
            card = self.get_top_sprite()
            if not by_open:
                card.flip()
            cards_set.addCard(card)
            self.remove(card)
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
            pile.remove(card)
            pile.cards.remove(card)
