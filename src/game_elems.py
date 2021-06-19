import pygame

from params import WIDTH, HEIGHT, CARD_W, CARD_H, MAGIC_CONST
from cards import Badge

class Pile(pygame.sprite.LayeredUpdates):
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)
        self.pos = [WIDTH - CARD_W, HEIGHT/2 - CARD_H/2]
    
    def addCard(self, card):
        self.add(card)        
        card.setTargetPos(self.pos)        
        self.change_layer(card, 1)

    def putToDeck(self, deck):
        while len(self.sprites()) > 0:
            card = self.get_top_sprite()
            deck.cards.append(card)
            card.setTargetPos([0, 0])
            self.remove(card)
    

class Stock(pygame.sprite.LayeredUpdates):
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)  
        self.pos = [0, HEIGHT/2 - CARD_H/2]
        
    def addCard(self, card):
        self.add(card)
        card.setTargetPos(self.pos)        
        self.change_layer(card, 1)
    
    def showTrump(self):        
        last_card = self.get_top_sprite()
        last_card.flip()
        last_card.setTargetPos([self.pos[0], self.pos[1] + CARD_W/4])
        last_card.image = pygame.transform.rotate(last_card.image, -90)
        self.change_layer(last_card, 0)
        # TODO: check is this correct!
        trump_badge = Badge(last_card.suit)
        self.add(trump_badge)
        
        return last_card.suit
    
    # TODO: change indecies 'n' because last sprite is badge of trump!
    def getCard(self, by_open = False):
        n = len(self.sprites())        
        if n > 0:
            card = self.get_top_sprite()              
            if n == 1:
                card.image = pygame.transform.rotate(card.image, 90)
                self.move_to_front(card)
            else:
                card.flip()
            if not by_open:
                card.flip()
            self.remove(card)
        else:
            card = []
        return card


class Table(pygame.sprite.LayeredUpdates):
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)  
        self.pos = [WIDTH/2 -  MAGIC_CONST*CARD_W/2, 13/8*CARD_H]
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
        while len(self.sprites()) > 0:
            card = self.get_top_sprite()
            if not by_open:
                card.flip()
            cards_set.addCard(card)
            self.remove(card)
        self.last_down = 0
        self.last_up   = 0
