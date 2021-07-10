import pygame
import os
from pathlib import Path
from enum import IntEnum, Enum, Flag

from params import MESSAGE_BOX_COLOR

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
    def __init__(self, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.target_pos = pos
        
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

# class Card-Sprite
class CardS(Card, ItemS):        
    def __init__(self, suit, rank):
        Card.__init__(self, suit, rank)        
        p = os.path.join(img_folder, suit.value, str(rank.value) + '.png')
        # print(p)
        face = pygame.image.load(p).convert()
        back = pygame.image.load(os.path.join(img_folder, 'back.png')).convert()
        self.sides = [back, face]
        ItemS.__init__(self, self.sides[0], [0, 0])      
        #TODO: set background color CLOTH_COLOR
        
    def flip(self):
        Card.flip(self)
        self.sides[0], self.sides[1] = self.sides[1], self.sides[0]
        self.image = self.sides[0]

class Badge(ItemS):
    def __init__(self, suit, pos):
        b = pygame.image.load(os.path.join(img_folder, suit.value, 'badge.png')).convert()
        ItemS.__init__(self, b, pos)
        
class TextBox(ItemS):
    def __init__(self, pos, size):
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        img = pygame.Surface(size)
        img.fill(MESSAGE_BOX_COLOR)
        ItemS.__init__(self, img, pos)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        
    def setText(self, text):
        self.text = self.font.render(text, True, (0,0,0)) 
        
    def draw(self, screen):
        pygame.draw.rect(screen, MESSAGE_BOX_COLOR, self.rect)
        text_rect = self.text.get_rect(center = self.getCenter())
        screen.blit(self.text, text_rect)
    
    def getCenter(self):
        s = self.image.get_size()
        p = [self.rect.x, self.rect.y]
        return [p[0] + s[0]/2, p[1] + s[1]/2]