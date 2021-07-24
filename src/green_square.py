import pygame

from params import WIDTH, HEIGHT, FPS, COLOR_CLOTH 
from elems  import Deck, Pile, Stock, Table, Dealer
from player import Status
from user   import User
from ai     import NikitaA
from rules  import GameStage, reactToMove, isGameOver, whoIsFool

# TODO: write log file contained all moves of players and their cards on hands
# TODO: create a text file with a win score between each AI and user
# TODO: customize 'new game' by press 'N' key after 'game over'
     
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fool Game")


clock = pygame.time.Clock()

deck = Deck()
    
pl1 = User("Alexey_V", 1)
pl2 = NikitaA(2)
players = {'active': pl1, 'passive': pl2}
stock     = Stock()
pile      = Pile()
table     = Table()

game_stage = GameStage.START
running = True
while running:
    clock.tick(FPS)
        
    for event in pygame.event.get():        
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n and game_stage == GameStage.START:
                deck.shuffle()
                trump = Dealer.deal(deck, players, stock)
                game_stage = GameStage.PLAYING  
                players['active'].status  = Status.ATTACKER
                players['passive'].status = Status.DEFENDING                    
                
            if event.key == pygame.K_SPACE and game_stage == GameStage.GAME_OVER:
                Dealer.all2deck(players, table, pile, deck)
                game_stage = GameStage.START
                pl1.mess_box.setText('')
                pl2.mess_box.setText('')
                
            if players['active'] == pl1 and game_stage == GameStage.PLAYING:
                mv = pl1.move(event, table, stock.vol(), pl2.vol())
                if not mv == []:
                    game_stage = reactToMove(players, table, pile, stock, mv)
                    if game_stage == GameStage.PLAYING:
                        start_ticks = pygame.time.get_ticks()
                        pl2.mess_box.setText('')
    
    # if pl2 is AI
    if players['active'] == pl2 and game_stage == GameStage.PLAYING:
        sec = (pygame.time.get_ticks()-start_ticks)/1000
        if sec > 1:
            mv = pl2.move(table, stock.vol(), pl1.vol())
            game_stage = reactToMove(players, table, pile, stock, mv)
            if game_stage == GameStage.PLAYING:
                start_ticks = pygame.time.get_ticks()
                pl1.mess_box.setText('')

    deck.update()
    pl1.update()
    pl2.update()
    stock.update()
    table.update()
    pile.update()
    
    screen.fill(COLOR_CLOTH)
    
    deck.draw(screen)    
    pl1.draw(screen)  
    pl2.draw(screen)  
    stock.draw(screen)
    table.draw(screen)
    pile.draw(screen)
    
    pygame.display.flip()
    

pygame.quit()