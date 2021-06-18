import pygame

from cards import Deck

WIDTH = 960
HEIGHT = 640
FPS = 30

CLOTH_COLOR = (46, 139, 87)
FRAME_COLOR = (128, 128, 0)

  
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fool Game")


clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

deck = Deck()
# deck.shuffle()
for c in deck.cards:
    all_sprites.add(c)
    
n = 1
running = True
while running:
    clock.tick(FPS)
        
    for event in pygame.event.get():        
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
       

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and n < 36:
                c = deck.cards.pop()
                c.turnOver()
                c.setTargetPos([10*n, 0])
                n += 1
                print(n)
            

    all_sprites.update()
    
    screen.fill(CLOTH_COLOR)
    
    all_sprites.draw(screen)    
    
    pygame.display.flip()
    

pygame.quit()