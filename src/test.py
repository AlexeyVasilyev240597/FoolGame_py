import pygame

from params import WIDTH, HEIGHT, FPS, CLOTH_COLOR, FRAME_COLOR
from items import Suit, Rank, Badge
from elems import Deck, Pile, Stock, Table, Dealer
  
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fool Game")


clock = pygame.time.Clock()

deck = Deck()
    
stock = Stock()
table = Table()
pile = Pile()
    
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
                #c = deck.getFromTop()
                c = stock.getCard()
                c.flip()
                c.setTargetPos([20*n, 0])
                n += 1

            if event.key == pygame.K_n:
                Dealer.deck2stock(deck, stock)
                trump = stock.showTrump()
            if event.key == pygame.K_m:
                while len(stock.sprites()) > 1:
                    pile.addCard(stock.getCard())
            if event.key == pygame.K_k:
                Dealer.pile2deck(pile, deck)

            
    deck.update()
    stock.update()
    pile.update()
    
    screen.fill(CLOTH_COLOR)
    
    deck.draw(screen)
    stock.draw(screen)  
    pile.draw(screen)
    
    pygame.display.flip()
    

pygame.quit()