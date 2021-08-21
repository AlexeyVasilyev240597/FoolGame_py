import pygame
from enum import IntEnum

from params import CARD_H, CARD_W, PLAYER_H, PLAYER_W, POS_PLAYERS, FLAG_DEBUG
from params import COLOR_FRAME
from params import MAGIC_CONST
from items import Rank, TextBox
from elems import Element

class Status(IntEnum):
    ATTACKER  = 1
    DEFENDING = 2
    ADDING    = 3
    FOOL      = 4

class Word(IntEnum):
    BEATEN    = 1
    TAKE      = 2
    TAKE_AWAY = 3       

class PlayerAsRival:
    def __init__(self, name, vol, status, last_move):
        self.name      = name
        self.vol       = vol
        self.status    = status
        self.last_move = last_move

class Player(Element):
    # counter of players
    counter = 0
    def __init__(self, name, is_user = True):
        Player.counter += 1
        
        # main params        
        self.name = name
        self.status = []
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
        
        # game params
        self.trump = []
        self.table = []
        self.get_weight = lambda card : ((card.suit == self.trump)*
                                         Rank.ACE.value + card.rank.value)
        self.losing_counter = 0
        self.last_move = {}
        
        # info boxes params
        box_size = [2*CARD_W, CARD_H/3]
        box_pos  = self.loc2glob([self.w + self.t, 0])    
        
        self.name_box = TextBox(box_pos, box_size)
        self.name_box.setText(name)
        
        box_pos  = self.loc2glob([self.w + self.t, box_size[1] + self.t])        
        self.mess_box = TextBox(box_pos, box_size)
        
        box_pos  = self.loc2glob([self.w + self.t, 2*box_size[1] + self.t])        
        self.score_box = TextBox(box_pos, box_size)
        
    def addCard(self, card):
        Element.addCard(self, card)
        self.updateCards() 
        
    def getCard(self, indx = 0):
        flip_flag = not (FLAG_DEBUG ^ (self.status == Status.FOOL))
        card = Element.getCard(self, flip_flag, indx)
        self.updateCards()
        return card
        
    def showCard(self, indx):
        pass
    
    def _showCard(self, indx):
        if indx < self.vol():
            return self._cards.sprites()[indx]
        
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
        
    def setNewGameParams(self, trump, table, status):
        self.trump  = trump        
        self.table  = table
        self.status = status
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
    
    def iAmFool(self):
        self.status = Status.FOOL
        self.losing_counter += 1
        self.mess_box.setText('Я Дурак!')
        self.score_box.setText('Дурак ' + str(self.losing_counter) + ' раз(а)')
    
    def getMeAsRival(self):
        return PlayerAsRival(self.name, 
                             self.vol(), 
                             self.status, 
                             self.last_move)
    
    def updateCards(self):        
        cards = sorted(self._cards, key = self.get_weight)
        v = self.vol()
        for l, c in zip(range(v), cards):
            self._cards.change_layer(c, l)
            pos_loc = self.getCardPos(self._cards.get_layer_of_sprite(c))
            pos = self.loc2glob(pos_loc)
            c.setTargetPos(pos)
            
    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_FRAME, self.rect, self.t)  
        Element.draw(self, screen)
        self.name_box.draw(screen)
        self.mess_box.draw(screen)
        self.score_box.draw(screen)