import pygame

from params import WIDTH, HEIGHT, FPS, COLOR_CLOTH
from elems  import Deck, Pile, Stock, Table, Dealer
from user   import User
from ai     import AIGenerator
from rules  import GameStage, reactToMove, setNewGame, isGameOver, whoIsFool

# in seconds
TIME_DELAY = 1

# TODO: write log file (json) contained all moves of players and their cards on hands
# TODO: create a text file with a win score between each AI and user
# TODO: create a ring for AIs fighting 
#       (for minimization allocated resouces maybe it needs splitting 
#        kernel and graphic parts of Element class and its childern)
# TODO: write class Fool() or function fool() with all this code;
#       its params will be names of players
#       it will run in __main__ like here https://habr.com/ru/post/456214/
# TODO: put .py files to folders and write __init__ and __main__ funcs
     
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fool Game")


clock = pygame.time.Clock()

deck = Deck()

# AI_list = [Nikita_A, Alexander_P, George_P, Sergey_C, Gregory_P]    
pl1 = User("Alexey_V")
pl2 = AIGenerator('Sergey_C')
players = {'actv': pl1, 'pssv': pl2}
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
            if game_stage == GameStage.START and event.key == pygame.K_n:
                deck.shuffle()
                trump = Dealer.deal(deck, players, stock)
                setNewGame(players, trump, table)
                game_stage = GameStage.PLAYING  
                start_ticks = pygame.time.get_ticks()
                
            if game_stage == GameStage.PLAYING and players['actv'].is_user:
                pl_cur = players['actv']
                pl_riv = players['pssv']
                mv = pl_cur.move(event, stock.vol(), pl_riv.getMeAsRival())
                if not mv == []:
                    game_stage = reactToMove(players, table, pile, stock, mv)
                    if game_stage == GameStage.PLAYING:
                        start_ticks = pygame.time.get_ticks()
                        pl_riv.mess_box.setText('')
                    elif game_stage == GameStage.GAME_OVER:
                        whoIsFool(players)
            
            if game_stage == GameStage.GAME_OVER and event.key == pygame.K_SPACE:
                Dealer.all2deck(players, table, pile, deck)
                game_stage = GameStage.START
                pl1.mess_box.setText('')
                pl2.mess_box.setText('')
                stock.trump_badge.empty()
                
    
    if not players['actv'].is_user and game_stage == GameStage.PLAYING:
        pl_cur = players['actv']
        pl_riv = players['pssv']
        sec = (pygame.time.get_ticks()-start_ticks)/1000
        if sec > TIME_DELAY:
            mv = pl_cur.move(stock.vol(), pl_riv.getMeAsRival())
            game_stage = reactToMove(players, table, pile, stock, mv)
            if game_stage == GameStage.PLAYING:
                start_ticks = pygame.time.get_ticks()
                pl_riv.mess_box.setText('')
            elif game_stage == GameStage.GAME_OVER:
                whoIsFool(players)
    
    pl1.update()
    pl2.update()
    stock.update()
    table.update()
    pile.update()
    deck.update()
    
    screen.fill(COLOR_CLOTH)
        
    pl1.draw(screen)  
    pl2.draw(screen)  
    stock.draw(screen)
    table.draw(screen)
    pile.draw(screen)
    deck.draw(screen)
    
    pygame.display.flip()
    

pygame.quit()