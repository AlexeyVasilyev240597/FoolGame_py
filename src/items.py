import pygame
import os
from pathlib import Path
from enum import IntEnum, Enum, Flag

from params import COLOR_MESSAGE_BOX

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

DECK_VOLUME = len(Rank)*len(Suit)
    
class Side(Flag):
    BACK = 0
    FACE = 1

class Card:        
    def __init__(self, suit, rank, side = Side.BACK):
        self.suit = suit
        self.rank = rank
        self.side = side

    def __repr__(self):
        if self.side == Side.FACE:
            if self.rank.value == Rank.JACK:
                rank = 'J'
            elif self.rank.value == Rank.QUEEN:
                rank = 'Q'
            elif self.rank.value == Rank.KING:
                rank = 'K'
            elif self.rank.value == Rank.ACE:
                rank = 'A'
            else:
                rank = str(self.rank.value)
            return repr(rank + '-' + self.suit.value)
        else:
            # unknown
            return repr('UNK')

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
            # Normal
            N = [self.target_pos[0] - self.rect.x, self.target_pos[1] - self.rect.y]
            # length of way to target position in pixels
            L = abs(N[0]) + abs(N[1])
            # number of pixels per shot
            dl = min(15, L)
            dx = round(N[0]/L*dl)
            dy =   int(N[1]/L*dl)
            self.rect.x += dx
            self.rect.y += dy

# class Card-Sprite
class CardS(Card, ItemS):        
    def __init__(self, suit, rank):
        Card.__init__(self, suit, rank)        
        p2f = os.path.join(img_folder, suit.value, str(rank.value) + '.png')
        face = pygame.image.load(p2f).convert()
        p2b = os.path.join(img_folder, 'back.png')
        back = pygame.image.load(p2b).convert()
        self.sides = [back, face]
        ItemS.__init__(self, self.sides[0], [0, 0])      
        #TODO: set background color CLOTH_COLOR

    def flip(self):
        Card.flip(self)
        self.sides[0], self.sides[1] = self.sides[1], self.sides[0]
        self.image = self.sides[0]

class Badge(ItemS):
    def __init__(self, suit, pos):
        p2b = os.path.join(img_folder, suit.value, 'badge.png')
        b = pygame.image.load(p2b).convert()
        ItemS.__init__(self, b, pos)

class TextBox:
    def __init__(self, pos, size):
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.pos = pos
        self.size = size
        self.center = [self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2]
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.text = []

    def setText(self, text):
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_MESSAGE_BOX, self.rect)
        if not self.text == []:
            text_r = self.font.render(self.text, True, (0,0,0)) 
            text_rect = text_r.get_rect(center = self.center)
            screen.blit(text_r, text_rect)