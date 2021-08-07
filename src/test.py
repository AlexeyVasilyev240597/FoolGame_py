
from params import MAGIC_CONST
from items  import Suit, Rank
from elems  import Deck, Pile, Stock, Table, Dealer
from ai     import getAIinstance
from rules  import setStatusInNewGame
from logger import Logger
  
deck = Deck()
# deck.shuffle()

stock = Stock()
table = Table()
pile = Pile()


pl_1 = getAIinstance('Nikita_A')
pl_2 = getAIinstance('Sergey_C')
players = {'actv': pl_1, 'pssv': pl_2}
trump = Dealer.deal(deck, players, stock)
setStatusInNewGame(players)

log = Logger(1)
log.newGame(pl_1, pl_2, stock)
mv = pl_1.move(table, stock.vol(), pl_2.vol())
log.setMove(mv, pl_1, table, stock)
log.saveToFile()

# n = 1
# running = True
# while running:
#     clock.tick(FPS)
        
#     for event in pygame.event.get():        
#         # check for closing window
#         if event.type == pygame.QUIT:
#             running = False
       

#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE and n <= 36:
#                 # c = deck.getCard(True)
#                 # c = deck.getFromBottom()
#                 c = stock.getCard(True)
#                 # print(c)
#                 # c = stock.getCard()
#                 c.setTargetPos([20*n, 0])
#                 n += 1

#             if event.key == pygame.K_n:
#                 Dealer.deck2stock(deck, stock)
#                 trump = stock.showTrump()
#             # if event.key == pygame.K_m:
#             #     while len(stock.sprites()) > 1:
#             #         pile.addCard(stock.getCard())
#             # if event.key == pygame.K_k:
#             #     Dealer.pile2deck(pile, deck)

#     all_sprites.update()
#     deck.update()
#     stock.update()
#     # pile.update()
#     # b.update()
    
#     screen.fill(CLOTH_COLOR)
    
#     all_sprites.draw(screen)
#     deck.draw(screen)
#     stock.draw(screen)  
#     # pile.draw(screen)
#     # b.draw(screen)
    
#     pygame.display.flip()
    

# pygame.quit()