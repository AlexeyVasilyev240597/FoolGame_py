import pygame

from params import WIDTH, HEIGHT, FPS, COLOR_CLOTH
from elems  import Deck, Pile, Stock, Table, Dealer
from ai     import getAIinstance
from rules  import GameStage, reactToMove, setStatusInNewGame

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
while not game_stage == GameStage.GAME_OVER:
    clock.tick(FPS)
    
    if game_stage == GameStage.START:
        deck.shuffle()
        trump = Dealer.deal(deck, players, stock)
        game_stage = GameStage.PLAYING  
        setStatusInNewGame(players)
        start_ticks = pygame.time.get_ticks()
                
    if game_stage == GameStage.GAME_OVER:
        Dealer.all2deck(players, table, pile, deck)
        game_stage = GameStage.START                
    
    if not players['active'].is_user and game_stage == GameStage.PLAYING:
        pl_cur = players['active']
        pl_riv = players['passive']
        mv = pl_cur.move(table, stock.vol(), pl_riv.vol())
        game_stage = reactToMove(players, table, pile, stock, mv)
        if game_stage == GameStage.PLAYING:
            start_ticks = pygame.time.get_ticks()
            pl_riv.mess_box.setText('')

    screen.fill(COLOR_CLOTH)
    pygame.display.flip()

msec = pygame.time.get_ticks()-start_ticks    
print('one game: ', msec, ' ms')

pygame.quit()