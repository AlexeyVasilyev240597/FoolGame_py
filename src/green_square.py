from elems  import Deck, Pile, Stock, Table, Dealer
from ai     import AIGenerator
from rules  import GameStage, setStatusInNewGame, reactToMove, isGameOver, whoIsFool
from logger import Logger, LogMode

NUM_OF_GAMES = 1

deck = Deck()    
pl1 = AIGenerator('Nikita_A')
pl2 = AIGenerator('George_P')
players = {'actv': pl1, 'pssv': pl2}
stock     = Stock()
pile      = Pile()
table     = Table()

log = Logger(LogMode.SCORE)

game_stage = GameStage.START
for n in range(NUM_OF_GAMES):
    deck.shuffle()
    trump = Dealer.deal(deck, players, stock)
    setStatusInNewGame(players)
    log.newGame(pl1, pl2, stock)

    game_stage = GameStage.PLAYING      
    while game_stage == GameStage.PLAYING:
        mv = players['actv'].move(table, stock.vol(), players['pssv'].vol())        
        reactToMove(players, table, pile, stock, mv)
        game_stage = isGameOver(stock, players)
        log.setMove(mv, players['actv'], table, stock)
    
    fool_name = whoIsFool(players)
    log.setFool(fool_name)
    Dealer.all2deck(players, table, pile, deck)
    
log.setScore()  
log.saveToFile()