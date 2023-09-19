import os
from pathlib import Path
import pygame

from src.core.card import Card
from src.view.card_view import CardView

src_folder = Path(os.path.dirname(__file__)).parent.parent.parent
img_folder = os.path.join(src_folder, 'pic')

class CardViewGraph(CardView, pygame.sprite.Sprite):
    def __init__(self, card: Card, pos):
        CardView.__init__(self, card)
        if self.open:
            p2f = os.path.join(img_folder, 
                               self.suit.value,
                               str(self.rank.value) + '.png')
            self.image = pygame.image.load(p2f).convert()
        else:
            p2b = os.path.join(img_folder, 'back.png')
            self.image = pygame.image.load(p2b).convert()
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.target_pos = pos
    
    def cardView2card(card_view):
        return Card(CardViewGraph.suit, CardViewGraph.rank)
    
    
    def draw(self):
        pass
    
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
