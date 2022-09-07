from enum import IntEnum

from params import MAGIC_CONST, FLAG_DEBUG
from elems  import Dealer
from player import Role, Status, Word

class GameStage(IntEnum):
    START     = 1
    PLAYING   = 2
    GAME_OVER = 3

def swapRole(players):
    players[Role.ACTV], players[Role.PSSV] = players[Role.PSSV], players[Role.ACTV]
    
# now first move is given
#   to first by order player in first game,
#   to winner if he is,
#   to player which throws last card if dead heat
def setNewGame(deck, stock, table, players):
    deck.shuffle()
    Dealer.deal(deck, players[Role.ACTV], players[Role.PSSV], stock)
    players[Role.ACTV].setNewGameParams(stock.trump, table, Status.ATTACKER)
    players[Role.PSSV].setNewGameParams(stock.trump, table, Status.DEFENDING)
    return GameStage.PLAYING

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

def how_many_add_from_stock(pv, s):
    dv = {Role.ACTV: 0, Role.PSSV: 0}
    while s > 0 and (pv[Role.ACTV] < MAGIC_CONST or pv[Role.PSSV] < MAGIC_CONST):
        if pv[Role.ACTV] < pv[Role.PSSV]:
            dv[Role.ACTV] += 1
            pv[Role.ACTV] += 1
        else:
            dv[Role.PSSV] += 1
            pv[Role.PSSV] += 1
        s -= 1
    return dv

def addFromStock(players, stock):
    pv = {Role.ACTV: players[Role.ACTV].vol(), Role.PSSV: players[Role.PSSV].vol()}
    s  = stock.vol()
    dv = how_many_add_from_stock(pv, s)
    for role in players:
        for i in range(dv[role]):
            # if FLAG_DEBUG:
            #     players[role].addCard(stock.getCard(True))
            # else:
            players[role].addCard(stock.getCard(players[role].is_user))

def isGameOver(stock, players):
    stock_vol = stock.vol()
    p1_vol    = players[Role.ACTV].vol()
    p2_vol    = players[Role.PSSV].vol()
    if stock_vol == 0 and (p1_vol == 0 or p2_vol == 0):        
        return GameStage.GAME_OVER
    else:
        return GameStage.PLAYING

def whoIsFool(players):
    p1_vol    = players[Role.ACTV].vol()
    p2_vol    = players[Role.PSSV].vol()
    if p1_vol == 0 and p2_vol == 0:
        players[Role.ACTV].mess_box.setText('Ничья!')
        players[Role.PSSV].mess_box.setText('Ничья!')
        return 'no one'
    elif p2_vol == 0:
        players[Role.ACTV].iAmFool()
        players[Role.PSSV].mess_box.setText('Лады')
        swapRole(players)
        return players[Role.PSSV].name
    elif p1_vol == 0:
        players[Role.ACTV].mess_box.setText('Лады')
        players[Role.PSSV].iAmFool()
        return players[Role.PSSV].name
    else: # wrong call
        return 'neither yet'


def reactToWord(word, players, table, pile, stock):
    if word == Word.BEATEN:
        table.getAllCards(pile)
        players[Role.ACTV].setStatus(Status.DEFENDING)
        players[Role.PSSV].setStatus(Status.ATTACKER)
        addFromStock(players, stock)
        swapRole(players)
    elif word == Word.TAKE:
        players[Role.PSSV].setStatus(Status.ADDING)
        swapRole(players)
    elif word == Word.TAKE_AWAY:
        # if FLAG_DEBUG:
        #     table.getAllCards(players[Role.PSSV], True)
        # else:
        table.getAllCards(players[Role.PSSV], players[Role.PSSV].is_user)
        players[Role.ACTV].setStatus(Status.ATTACKER)
        players[Role.PSSV].setStatus(Status.DEFENDING)
        addFromStock(players, stock)   
    return isGameOver(stock, players)

def reactToMove(players, table, pile, stock, mv):
    if 'card' in mv:
        card = mv.get('card')
        table.addCard(card, players[Role.ACTV].status == Status.DEFENDING)
        if not players[Role.ACTV].status == Status.ADDING:
            swapRole(players)
        game_stage = GameStage.PLAYING
    if 'word' in mv:
        word = mv.get('word')
        game_stage = reactToWord(word, players, table, pile, stock)
    return game_stage