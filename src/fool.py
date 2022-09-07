import pygame

from params  import WIDTH, HEIGHT, FPS, COLOR_CLOTH
from elems   import Deck, Pile, Stock, Table, Dealer
from player  import Role
from user    import User
from ai      import AIGenerator
from rules   import GameStage, reactToMove, setNewGame, whoIsFool
from context import PlayingContext

# TODO: create a text file with a win score between each AI and user
# TODO: create a ring for AIs fighting 
#       (for minimization allocated resouces maybe it needs splitting 
#        kernel and graphic parts of Element class and its childern)
# TODO: function play_fool_game() will run in __main__ 
#       like here https://habr.com/ru/post/456214/
# TODO: put .py files to folders and write __init__ and __main__ funcs
# TODO: create a flashing in TIME_DELAY of green frame of players button after its pressing

def play_fool_game(user_name, ai_name):
    # in seconds
    TIME_DELAY = 1
             
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fool Game")
    
    
    clock = pygame.time.Clock()
    
    deck = Deck()
      
    pl1       = User(user_name)
    pl2       = AIGenerator.getInstance(ai_name)
    players   = {Role.ACTV: pl1, Role.PSSV: pl2}
    stock     = Stock()
    pile      = Pile()
    table     = Table()
    
    game_stage = GameStage.START
    pl1.mess_box.setText('Начнём')
    running = True
    while running:
        clock.tick(FPS)
            
        for event in pygame.event.get():        
            # check for closing window
            if event.type == pygame.QUIT:                
                del pl1
                del pl2
                return

            if (event.type == pygame.MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                
                if (game_stage == GameStage.START):
                      user_clicked = pl1.mess_box.rect.collidepoint(pos) 
                      if user_clicked:
                        game_stage = setNewGame(deck, stock, table, players)
                        context = PlayingContext(stock.trump)
                        start_ticks = pygame.time.get_ticks()
                
                elif (game_stage == GameStage.PLAYING and
                    players[Role.ACTV].is_user):
                    if players[Role.ACTV].isClicked(pos):
                        # user's move
                        # pl_cur = players[Role.ACTV]
                        pl_riv = players[Role.PSSV]
                        mv = players[Role.ACTV].move(context)
                        if mv:
                            context = PlayingContext.netx_context(context, mv)
                            game_stage = reactToMove(players, table, pile, stock, mv)
                            if game_stage == GameStage.PLAYING:
                                start_ticks = pygame.time.get_ticks()
                                pl_riv.mess_box.setText('')
                            elif game_stage == GameStage.GAME_OVER:
                                whoIsFool(players)
                            print(repr(context))
                
                elif (game_stage == GameStage.GAME_OVER):
                    user_clicked = pl1.mess_box.rect.collidepoint(pos) 
                    if user_clicked:
                        Dealer.all2deck([players[Role.ACTV], players[Role.PSSV]], table, pile, deck)
                        game_stage = GameStage.START
                        stock.trump_badge.empty()
                        pl1.mess_box.setText('Ещё раз')
                        pl2.mess_box.setText('')
        
        if not players[Role.ACTV].is_user and game_stage == GameStage.PLAYING:
            sec = (pygame.time.get_ticks()-start_ticks)/1000
            if sec > TIME_DELAY:
                mv = players[Role.ACTV].move(context)
                context = PlayingContext.netx_context(context, mv)
                game_stage = reactToMove(players, table, pile, stock, mv)
                if game_stage == GameStage.PLAYING:
                    start_ticks = pygame.time.get_ticks()
                elif game_stage == GameStage.GAME_OVER:
                    whoIsFool(players)
                print(repr(context))
        
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