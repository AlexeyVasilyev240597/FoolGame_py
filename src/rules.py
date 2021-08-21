from enum import IntEnum

from params import MAGIC_CONST, FLAG_DEBUG
from player import Status, Word

# TODO: create structure for working with players

class GameStage(IntEnum):
    START     = 1
    PLAYING   = 2
    GAME_OVER = 3

def swapRole(players):
    players['actv'], players['pssv'] = players['pssv'], players['actv']
    
# now first move is given
#   to first by order player in first game,
#   to winner if he is,
#   to player which throws last card if dead heat
def setNewGame(players, trump, table):    
    players['actv'].setNewGameParams(trump, table, Status.ATTACKER)
    players['pssv'].setNewGameParams(trump, table, Status.DEFENDING)

# PARAM INPUT:
#   status of actv player (which threw card)
#   table is object with actual state of table
#   card (thrown)
#   trump in game
# PARAM OUT:
#   answer: is chosen card correct
def isChoiceCorrect(status, table, card, trump):
    if status == Status.ATTACKER and table.vol() == 0:
        return True
    if status == Status.ATTACKER or status == Status.ADDING:
        for n in range(table.vol('up')):
            c = table.showCard('up', n)
            if card.rank == c.rank:
                return True    
        for n in range(table.vol('down')):
            c = table.showCard('down', n)
            if card.rank == c.rank:
                return True   
        return False
    if status == Status.DEFENDING:
        last = table.showCard('down', table.vol('down')-1)
        return (last.suit == card.suit and last.rank < card.rank or 
                not (last.suit == card.suit) and (card.suit == trump))

# PARAM IN:
#   status of actv player (which threw card)
#   table is object with actual state of table
#   rival_vol is number of cards in rival's hand
# PARAM OUT:
#   answer: can card be thrown to table
def canCardBeThrown(status, table, rival_vol):
    # 6*2 = 12 cards on table => ATTACKER should say BEATEN
    # or DEFENDING player do not have cards
    # number of cards added by ADDING player on table equals 
    # number of taking player's cards => ADDING should say TAKE_AWAY
    if ((status == Status.ATTACKER or status == Status.ADDING) and 
        ((table.vol('down') - table.vol('up')) == rival_vol or 
          table.vol('down') == MAGIC_CONST)):
            return False
    return True


def addFromStock(players, stock):
    pv = {'actv': players['actv'].vol(), 'pssv': players['pssv'].vol()}
    dv = {'actv': 0, 'pssv': 0}
    s  = stock.vol()
    while s > 0 and (pv['actv'] < MAGIC_CONST or pv['pssv'] < MAGIC_CONST):
        if pv['actv'] < pv['pssv']:
            dv['actv'] += 1
            pv['actv'] += 1
        else:
            dv['pssv'] += 1
            pv['pssv'] += 1
        s -= 1    
    for role in players:       
        for i in range(dv[role]):
            if FLAG_DEBUG:
                players[role].addCard(stock.getCard(True))
            else:
                players[role].addCard(stock.getCard(players[role].is_user))

def isGameOver(stock, players):
    stock_vol = stock.vol()
    p1_vol    = players['actv'].vol()
    p2_vol    = players['pssv'].vol()
    if stock_vol == 0 and (p1_vol == 0 or p2_vol == 0):        
        return GameStage.GAME_OVER
    else:
        return GameStage.PLAYING

def whoIsFool(players):
    p1_vol    = players['actv'].vol()
    p2_vol    = players['pssv'].vol()
    if p1_vol == 0 and p2_vol == 0:
        return 'no one'
    elif p2_vol == 0:
        players['actv'].iAmFool()
        swapRole(players)
        return players['pssv'].name
    elif p1_vol == 0:
        players['pssv'].iAmFool()
        return players['pssv'].name
    else: # wrong call
        return 'neither yet'


def reactToWord(word, players, table, pile, stock):
    if word == Word.BEATEN:
        table.shift(pile, True)
        players['actv'].status  = Status.DEFENDING
        players['pssv'].status = Status.ATTACKER
        addFromStock(players, stock)
        swapRole(players)
    if word == Word.TAKE:
        players['pssv'].status = Status.ADDING
        swapRole(players)
    if word == Word.TAKE_AWAY:
        if FLAG_DEBUG:
            table.shift(players['pssv'], False)
        else:
            table.shift(players['pssv'], not players['pssv'].is_user)
        players['actv'].status  = Status.ATTACKER
        players['pssv'].status = Status.DEFENDING
        addFromStock(players, stock)   
    return isGameOver(stock, players)

def reactToMove(players, table, pile, stock, mv):
    game_stage = GameStage.PLAYING
    if 'card' in mv:
        card = mv.get('card')
        table.addCard(card, players['actv'].status == Status.DEFENDING)
        if not players['actv'].status == Status.ADDING:
            swapRole(players)
    if 'word' in mv:
        word = mv.get('word')
        game_stage = reactToWord(word, players, table, pile, stock)
    return game_stage