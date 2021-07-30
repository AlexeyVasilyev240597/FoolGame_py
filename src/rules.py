from enum import IntEnum

from params import MAGIC_CONST, FLAG_DEBUG
from player import Status, Word

# TODO: create structure for working with players

class GameStage(IntEnum):
    START     = 1
    PLAYING   = 2
    GAME_OVER = 3

def swapRole(players):
    players['active'], players['passive'] = players['passive'], players['active']
    
# now first move is given
#   to first by order player in first game,
#   to winner if he is,
#   to player which throws last card if dead heat
def setStatusInNewGame(players):
    players['active'].status  = Status.ATTACKER
    players['passive'].status = Status.DEFENDING

# PARAM INPUT:
#   status of active player (which threw card)
#   table is object with actual state of table
#   card (thrown)
#   trump in game
# PARAM OUT:
#   answer: is chosen card correct
def isChoiceCorrect(status, table, card, trump):
    if status == Status.ATTACKER and table.vol() == 0:
        return True
    if status == Status.ATTACKER or status == Status.ADDING:
        for c in table.cards.sprites():
            if card.rank == c.rank:
                return True
        return False
    if status == Status.DEFENDING:
        last = table.cards.sprites()[-1]
        return ((last.suit == card.suit) and (last.rank < card.rank)) or (not (last.suit == card.suit) and (card.suit == trump))

# PARAM IN:
#   status of active player (which threw card)
#   table is object with actual state of table
#   rival_vol is number of cards in rival's hand
# PARAM OUT:
#   answer: can card be thrown to table
def canCardBeThrown(status, table, rival_vol):
    # 6*2 = 12 cards on table => ATTACKER should say BEATEN
    # or DEFENDING player do not have cards
    if table.last_down == MAGIC_CONST:
        return False
    # number of cards added by ADDING player on table equals 
    # number of taking player's cards => ADDING should say TAKE_AWAY
    if status == Status.ATTACKER or status == Status.ADDING:
        if (table.last_down - table.last_up) == rival_vol:
            return False
    return True


def addFromStock(players, stock):
    pv = {'active': players['active'].vol(), 'passive': players['passive'].vol()}
    dv = {'active': 0, 'passive': 0}
    s  = stock.vol()
    while s > 0 and (pv['active'] < MAGIC_CONST or pv['passive'] < MAGIC_CONST):
        if pv['active'] < pv['passive']:
            dv['active'] += 1
            pv['active'] += 1
        else:
            dv['passive'] += 1
            pv['passive'] += 1
        s -= 1    
    for role in players:       
        for i in range(dv[role]):
            if FLAG_DEBUG:
                players[role].addCard(stock.getCard(True))
            else:
                players[role].addCard(stock.getCard(players[role].is_user))

def isGameOver(stock, players):
    stock_vol = stock.vol()
    p1_vol    = players['active'].vol()
    p2_vol    = players['passive'].vol()
    return stock_vol == 0 and (p1_vol == 0 or p2_vol == 0)

def whoIsFool(players):
    p1_vol    = players['active'].vol()
    p2_vol    = players['passive'].vol()
    if p1_vol == 0 and p2_vol == 0:
        players['active'].mess_box.setText('Ничья!')
        players['passive'].mess_box.setText('Ничья!')
        return 'nobody'
    elif p2_vol == 0:
        # call yourself Fool
        players['active'].status = Status.FOOL
        players['active'].mess_box.setText('Я Дурак!') 
        players['active'].losing_counter += 1
        players['active'].setScore()
        # call him Fool
        players['passive'].mess_box.setText('Ты Дурак!')
        swapRole(players)
        return players['passive'].name
    elif p1_vol == 0:
        # call yourself Fool
        players['passive'].status = Status.FOOL
        players['passive'].mess_box.setText('Я Дурак!')
        players['passive'].losing_counter += 1
        players['passive'].setScore()
        # call him Fool
        players['active'].mess_box.setText('Ты Дурак!')
        return players['passive'].name
    else: # wrong call
        return 'neither yet'


def reactToWord(word, players, table, pile, stock):
    if word == Word.BEATEN:
        table.getAllCards(pile)
        players['active'].status  = Status.DEFENDING
        players['passive'].status = Status.ATTACKER
        addFromStock(players, stock)
        swapRole(players)
    if word == Word.TAKE:
        players['passive'].status = Status.ADDING
        swapRole(players)
    if word == Word.TAKE_AWAY:
        if FLAG_DEBUG:
            table.getAllCards(players['passive'], True)
        else:
            table.getAllCards(players['passive'], players['passive'].is_user)
        players['active'].status  = Status.ATTACKER
        players['passive'].status = Status.DEFENDING
        addFromStock(players, stock)
    if isGameOver(stock, players):
        print(whoIsFool(players) + ' is the Fool!')
        return GameStage.GAME_OVER
    else:
        return GameStage.PLAYING

def reactToMove(players, table, pile, stock, mv):
    game_stage = GameStage.PLAYING
    if 'card' in mv:
        card = mv.get('card')
        table.addCard(card, players['active'].status == Status.DEFENDING)
        if not players['active'].status == Status.ADDING:
            swapRole(players)
    if 'word' in mv:
        word = mv.get('word')
        game_stage = reactToWord(word, players, table, pile, stock)
    return game_stage