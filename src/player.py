import pygame
from enum import IntEnum

from params import CARD_H, CARD_W, PLAYER_H, PLAYER_W, POS_PLAYERS
from params import COLOR_FRAME
from params import MAGIC_CONST
from items import Rank, TextBox
from elems import Element

class Status(IntEnum):
    ATTACKER  = 1
    DEFENDING = 2
    ADDING    = 3
    TAKING    = 4
    FOOL      = 5
    
class Word(IntEnum):
    BEATEN    = 1
    TAKE      = 2
    TAKE_AWAY = 3       

class Player(Element):
    counter = 0
    def __init__(self, name, is_user = True):
        Player.counter += 1
        # main params        
        self.name = name
        self.status = []#Status(id)
        self.is_user = is_user
        # geometric params
        self.MAX_IN_ROW = 2*MAGIC_CONST
        if Player.counter == 1:
            pos = POS_PLAYERS['down']
        else: # Player.counter == 2
            pos = POS_PLAYERS['up']
        self.h = PLAYER_H
        self.w = PLAYER_W
        self.rect = pygame.Rect(pos[0], pos[1], self.w, self.h)
        self.t = 4
        Element.__init__(self, pos)
        # info boxes params
        box_size = [2*CARD_W, CARD_H/3]
        box_pos  = self.loc2glob([self.w + self.t, 0])        
        self.name_box = TextBox(box_pos, box_size)
        self.name_box.setText(name)
        box_size = [2*CARD_W, CARD_H/3]
        box_pos  = self.loc2glob([self.w + self.t, self.h/2-box_size[1]/2])        
        self.mess_box = TextBox(box_pos, box_size)
        self.mess_box.setText('')
        # game params
        self.trump = []
        self.get_weight = lambda card : ((card.suit == self.trump)*Rank.ACE.value + card.rank.value)
        
    def addCard(self, card):
        Element.addCard(self, card)
        self.updateCards() 
                
    def getCardPos(self, layer):
        n = self.vol()
        if n == 1:
            x = 0
            y = 0
        else:
            # index of row
            ir = layer // self.MAX_IN_ROW
            y = int(CARD_H*ir/4)
                        
            # row number
            rn = n // self.MAX_IN_ROW
            if ir == rn:
                # number of elems in row
                nr = n % self.MAX_IN_ROW
            else:
                nr = self.MAX_IN_ROW
            
            # index of column
            ic = layer % self.MAX_IN_ROW
            if nr < MAGIC_CONST:
                x = ic*CARD_W
            else: # squeeze mode
                x = int((MAGIC_CONST-1)*CARD_W*ic/(nr-1))
        pos = [x, y]
        return pos
        
    def sayWord(self):
        if self.status == Status.ATTACKER:
            self.mess_box.setText('Бито!')
            return Word.BEATEN
        if self.status == Status.DEFENDING:
            self.mess_box.setText('Беру!')
            return Word.TAKE
        if self.status == Status.ADDING:
            # self.mess_box.setText('Забирай!')
            self.mess_box.setText('Бери!')
            return Word.TAKE_AWAY
        
    def setTrump(self, suit):
        self.trump = suit
        self.updateCards()

    def updateCards(self):        
        cards = sorted(self.cards, key = self.get_weight)
        v = self.vol()
        for l, c in zip(range(v), cards):
            self.cards.change_layer(c, l)
            pos_loc = self.getCardPos(self.cards.get_layer_of_sprite(c))
            pos = self.loc2glob(pos_loc)
            c.setTargetPos(pos)
            
    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_FRAME, self.rect, self.t)  
        Element.draw(self, screen)
        self.name_box.draw(screen)
        self.mess_box.draw(screen)