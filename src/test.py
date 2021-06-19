import pygame

from params import WIDTH, HEIGHT, FPS, CLOTH_COLOR, FRAME_COLOR
from cards import Suit, Rank, Deck, Badge
from game_elems import Pile, Stock, Table
  
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fool Game")


clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

k = 0
badges = []
for s in Suit:
    b = Badge(s)
    b.setTargetPos([200*k, 3*HEIGHT/4])
    badges.append(b)
    all_sprites.add(b)
    k += 1

deck = Deck()
# deck.shuffle()
for c in deck.cards:
    all_sprites.add(c)
    
pille = Pile()
stock = Stock()
table = Table()
    
n = 1
running = True
while running:
    clock.tick(FPS)
        
    for event in pygame.event.get():        
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
       

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and n <= 36:
                c = deck.cards.pop()
                c.flip()
                c.setTargetPos([20*n, 0])
                n += 1
                
            # TODO: write test for stock!
            if event.key == pygame.K_n:
                deck.putToPile(stock)
                trump = stock.showTrump()

            

    all_sprites.update()
    
    screen.fill(CLOTH_COLOR)
    
    all_sprites.draw(screen)    
    
    pygame.display.flip()
    

pygame.quit()