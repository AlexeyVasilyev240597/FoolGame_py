import pygame

from params import WIDTH, HEIGHT, FPS, COLOR_CLOTH
from elems  import Deck, Pile, Stock, Table, Dealer
from ai     import getAIinstance
from rules  import GameStage, reactToMove, setStatusInNewGame

NUMBER_OF_GAMES = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fool Game")

clock = pygame.time.Clock()

deck = Deck()

pl1 = getAIinstance('Nikita_A')
pl2 = getAIinstance('Sergey_C')
players = {'active': pl1, 'passive': pl2}
stock     = Stock()
pile      = Pile()
table     = Table()

game_stage = GameStage.START
running = True
games_counter = 0
start_ticks = pygame.time.get_ticks()
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():        
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    
    if game_stage == GameStage.START:
        deck.shuffle()
        trump = Dealer.deal(deck, players, stock)
        game_stage = GameStage.PLAYING  
        setStatusInNewGame(players)        
                
    if game_stage == GameStage.GAME_OVER:
        Dealer.all2deck(players, table, pile, deck)
        games_counter += 1
        if games_counter < NUMBER_OF_GAMES:
            game_stage = GameStage.START
    
    if not players['active'].is_user and game_stage == GameStage.PLAYING:
        pl_cur = players['active']
        pl_riv = players['passive']
        mv = pl_cur.move(table, stock.vol(), pl_riv.vol())
        game_stage = reactToMove(players, table, pile, stock, mv)

    if games_counter == NUMBER_OF_GAMES:
        pl1.name_box.draw(screen)
        pl1.score_box.draw(screen)
        pl2.name_box.draw(screen)
        pl2.score_box.draw(screen)        

    screen.fill(COLOR_CLOTH)
        
    pygame.display.flip()
    

msec = pygame.time.get_ticks() - start_ticks    
print('one game: ', msec, ' ms')

pygame.quit()