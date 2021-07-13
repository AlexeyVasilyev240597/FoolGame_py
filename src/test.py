import pygame

from params import WIDTH, HEIGHT, FPS, CLOTH_COLOR, FRAME_COLOR
from items import Suit, Rank, Badge
from elems import Deck, Pile, Stock, Table, Dealer
  
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fool Game")


clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
deck = Deck()
deck.shuffle()
for c in deck.cards:
    all_sprites.add(c)    

stock = Stock()
# table = Table()
pile = Pile()

b = Badge(Suit.DIAMONDS, [0, WIDTH-40])

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
                # c = deck.getFromTop(True)
                # c = deck.getFromBottom()
                c = stock.getCard(True)
                # print(c)
                # c = stock.getCard()
                # c.flip()
                c.setTargetPos([20*n, 0])
                n += 1

            if event.key == pygame.K_n:
                Dealer.deck2stock(deck, stock)
                trump = stock.showTrump()
            # if event.key == pygame.K_m:
            #     while len(stock.sprites()) > 1:
            #         pile.addCard(stock.getCard())
            # if event.key == pygame.K_k:
            #     Dealer.pile2deck(pile, deck)

    all_sprites.update()
    deck.update()
    stock.update()
    # pile.update()
    # b.update()
    
    screen.fill(CLOTH_COLOR)
    
    all_sprites.draw(screen)
    deck.draw(screen)
    stock.draw(screen)  
    # pile.draw(screen)
    # b.draw(screen)
    
    pygame.display.flip()
    

pygame.quit()