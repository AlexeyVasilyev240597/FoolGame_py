from elems  import Deck, Pile, Stock, Table, Dealer
from ai     import AIGenerator
from rules  import GameStage, setNewGame, reactToMove, isGameOver, whoIsFool
from logger import Logger, LogMode

NUM_OF_GAMES = 100

deck = Deck()    
# AI_list = [Nikita_A, Alexander_P, George_P, Sergey_C, Gregory_P]
pl1       = AIGenerator('Nikita_A')
pl2       = AIGenerator('Sergey_C')
players   = {'actv': pl1, 'pssv': pl2}
stock     = Stock()
pile      = Pile()
table     = Table()

# ALL, ENDSPIEL, SCORE
log = Logger(LogMode.SCORE)

mw = 0
game_stage = GameStage.START
for n in range(NUM_OF_GAMES):
    deck.shuffle()
    trump = Dealer.deal(deck, players, stock)
    setNewGame(players, trump, table)
    log.newGame(pl1, pl2, stock)

    # it_was_endspiel = True
    game_stage = GameStage.PLAYING      
    while game_stage == GameStage.PLAYING:
        mv = players['actv'].move(stock.vol(), players['pssv'].getMeAsRival())                        
        reactToMove(players, table, pile, stock, mv)        
        log.setMove(mv, players['actv'], table, stock)
        game_stage = isGameOver(stock, players)    
        # if stock.vol() == 0 and it_was_endspiel:
        #     mw += pl2.getMeanWeight()
        #     it_was_endspiel = False
    
    fool_name = whoIsFool(players)
    
    log.setFool(fool_name)
    Dealer.all2deck(players, table, pile, deck)
    
# mw /= NUM_OF_GAMES
# print(pl2.name)
# print(mw)
    
log.setScore()  
log.saveToJson()