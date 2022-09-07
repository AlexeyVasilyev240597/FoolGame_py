import pygame
from enum import IntEnum

from params import CARD_H, CARD_W, PLAYER_H, PLAYER_W, POS_PLAYERS#, FLAG_DEBUG
from params import COLOR_FRAME
from params import MAGIC_CONST
from items  import Rank, TextBox
from elems  import Element

class Role(IntEnum):
    # active
    ACTV = 1
    # passive
    PSSV = 2
    # in a three hands game
    # cuckold
    #CKLD = 3

class Status(IntEnum):
    ATTACKER  = 1
    DEFENDING = 2
    ADDING    = 3
    FOOL      = 4

class Word(IntEnum):
    BEATEN    = 1
    TAKE      = 2
    TAKE_AWAY = 3
    I_AM_FOOL = 4

words_rus = {Word.BEATEN:    'Бито!',
            Word.TAKE:      'Беру!',
            Word.TAKE_AWAY: 'Бери!',
            Word.I_AM_FOOL: 'Я Дурак!'}

word_by_status = {Status.ATTACKER:  Word.BEATEN,
                  Status.DEFENDING: Word.TAKE,
                  Status.ADDING:    Word.TAKE_AWAY,
                  Status.FOOL:      Word.I_AM_FOOL}

class Player(Element):
    def __init__(self, name, is_user = True):
        # main params        
        self.name = name
        self.status = []
        self.cur_move  = []
        self.is_user = is_user
        
        # geometric params
        self.MAX_IN_ROW = 2*MAGIC_CONST
        if is_user:
            pos = POS_PLAYERS['down']
        else: # Player.counter == 2
            pos = POS_PLAYERS['up']
        self.h = PLAYER_H
        self.w = PLAYER_W
        self.rect = pygame.Rect(pos[0], pos[1], self.w, self.h)
        self.t = 4
        Element.__init__(self, pos)
        
        # game params
        self.trump = None
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
    
    
    def needUpdate(player_meth):
        def updateCards(self, *args, **kwargs):
            val = player_meth(self, *args, **kwargs)
            # start updating stuff
            cards = sorted(self._cards, key = self.get_weight)
            v = self.vol()
            for l, c in zip(range(v), cards):
                self._cards.change_layer(c, l)
                pos_loc = self.getCardPos(self._cards.get_layer_of_sprite(c))
                pos = self.loc2glob(pos_loc)
                c.setTargetPos(pos)
            # end updating stuff
            return val
        return updateCards
    
    @needUpdate
    def addCard(self, card):
        Element.addCard(self, card)
        
    @needUpdate
    def getCard(self, indx = 0):
        # flip_flag = not (FLAG_DEBUG ^ (self.status == Status.FOOL))
        flip_flag = not (self.is_user ^ (self.status == Status.FOOL))
        card = Element.getCard(self, flip_flag, indx)
        return card
        
    def showCard(self, indx):
        pass
    
    def _showCard(self, indx):
        if indx < self.vol():
            return self._cards.sprites()[indx]
    
    @needUpdate
    def sayWord(self):
        word = word_by_status[self.status]
        # if not self.is_use1r:
        self.mess_box.setText(words_rus[word])
        return word
    
    @needUpdate
    def setNewGameParams(self, trump, table, status):
        self.trump  = trump        
        self.table  = table
        self.setStatus(status)
        
    def setStatus(self, status):
        self.status = status
        if self.is_user:
            self.mess_box.setText(words_rus[word_by_status[status]])
    
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
        times = self.losing_counter
        times_case = ' раза' if (times % 5 > 1 and times % 5 < 5) else ' раз'
        self.score_box.setText('Дурак ' + str(times) + times_case)
    
    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_FRAME, self.rect, self.t)  
        Element.draw(self, screen)
        self.name_box.draw(screen)
        self.mess_box.draw(screen)
        self.score_box.draw(screen)