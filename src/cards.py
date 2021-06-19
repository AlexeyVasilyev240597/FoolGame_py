import pygame
import random
import os
from pathlib import Path
from enum import IntEnum, Enum, Flag

game_folder = Path(os.path.dirname(__file__)).parent
img_folder = os.path.join(game_folder, 'pic')

class Rank(IntEnum):
    SIX   = 6
    SEVEN = 7
    EIGHT = 8
    NINE  = 9
    TEN   = 10
    JACK  = 11
    QUEEN = 12 
    KING  = 13
    ACE   = 14

class Suit(Enum):
    DIAMONDS = 'D'
    HEARTS   = 'H'
    CLUBS    = 'C'
    SPADES   = 'S'
    
class Side(Flag):
    BACK = 0
    FACE = 1

class Card:        
    def __init__(self, suit, rank):        
        self.suit = suit
        self.rank = rank         
        self.side = Side.BACK
        
    def __repr__(self):
        if self.side == Side.FACE:
            return repr(self.rank.name + ' of ' + self.suit.name)
        else:
            return repr('unknown')
        
    def flip(self):
        self.side = Side(not self.side)

class ItemS(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.target_pos = [self.rect.x, self.rect.y]
        
    # ------------------- moving funcs -------------------
    def setTargetPos(self, pos):
        self.target_pos = pos

    def update(self):
        if not (self.target_pos[0] == self.rect.x and self.target_pos[1] == self.rect.y):
            N = [self.target_pos[0] - self.rect.x, self.target_pos[1] - self.rect.y]
            L = abs(N[0]) + abs(N[1])
            # number of pixels per shot
            dl = min(10, L)
            dx = round(N[0]/L*dl)
            dy =   int(N[1]/L*dl)
            self.rect.x += dx
            self.rect.y += dy

class CardS(Card, ItemS):        
    def __init__(self, suit, rank):
        Card.__init__(self, suit, rank)        
        p = os.path.join(img_folder, suit.value, str(rank.value) + '.png')
        # print(p)
        face = pygame.image.load(p).convert()
        back = pygame.image.load(os.path.join(img_folder, 'back.png')).convert()
        self.sides = [back, face]
        ItemS.__init__(self, self.sides[0])
        
    def flip(self):
        Card.flip(self)
        self.sides[0], self.sides[1] = self.sides[1], self.sides[0]
        self.image = self.sides[0]
        

class Badge(ItemS):
    def __init__(self, suit):
        pygame.sprite.Sprite.__init__(self)
        b = pygame.image.load(os.path.join(img_folder, suit.value, 'badge.png')).convert()
        ItemS.__init__(self, b)

class Deck:
    def __init__(self):
        self.cards = []
        for s in Suit:
            for r in Rank:
                c = CardS(s, r)
                self.cards.append(c)
                
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, cards_set, num = 1, by_open = False):
        if len(self.cards) >= num:
            for n in range(num):
                c = self.cards.pop(0)
                if by_open:
                    c.flip()
                cards_set.addCard(c)
    
    def putToPile(self, pile):
        while len(self.cards) > 0:
            pile.addCard(self.cards.pop())
            
