from enum import IntEnum

from card    import Card
from context import Context
# from game_exception import WrongInitException
from player  import Status, Word, Players


CARDS_KIT = 6

class GameStage(IntEnum):
    START     = 1
    PLAYING   = 2
    GAME_OVER = 3
    
# TODO:
# class WrongMoveTypes(IntEnum):

# TODO:
# class PlayersEnum(IntEnum):
#     NOBODY   = -1
#     PLAYER_1 =  0
#     PLAYER_2 =  1


## CARDS TRANSFERING FUNCTIONS

# if stock doesn't have enough cards then everyone will get equal amount
def howManyToComplete(context: Context):
    stock_vol = context.stock.vol
    # players volume
    actv_vol = context.players.actv.vol
    pssv_vol = context.players.pssv.vol
    # need to add
    actv_add = 0
    pssv_add = 0
    while stock_vol > 0 and (actv_vol < CARDS_KIT or pssv_vol < CARDS_KIT):
        if actv_vol < pssv_vol:
            actv_add += 1
            actv_vol += 1
        else:
            pssv_add += 1
            pssv_vol += 1
        stock_vol -= 1
    return actv_add, pssv_add


# now in first game first move is given to first player (by order),
#     if dead heat then to player which throws last card 
#     and to winner otherwise
def deal(context: Context):
    # TODO: uncommnet this line - just for debugging comment
    # context.deck.shuffle()
    context.deck.shift(context.players.actv, CARDS_KIT)
    context.deck.shift(context.players.pssv, CARDS_KIT)
    context.deck.shift(context.stock)
    trump = context.stock.setTrump()
    context.players.setNewGameParams(trump, context.players.fool_id)


# TODO: describe according to the rules
def complete(context: Context):
    actv_add, pssv_add = howManyToComplete(context)
    # firstly cards are adding to passive player
    context.deck.shift(context.players.pssv, pssv_add)
    # then to active one
    context.deck.shift(context.players.actv, actv_add)


# collecting cards from all elements back to deck,
# call in finish of Game
def collect(context: Context):
    context.players.actv.shift(context.deck)
    context.players.pssv.shift(context.deck)
    context.table.shift(context.deck)
    context.stock.shift(context.deck)


## CHECKING PLAYER'S MOVE FUNCTIONS

# PARAM INPUT:
#   card (thrown)
#   game context
# PARAM OUT:
#   answer: is chosen card correct
def doesCardFit(card: Card, context: Context) -> bool:
    status = context.players.actv.status
    if (status == Status.ATTACKER and
        context.table.vol() == 0):
        return True
    if (status == Status.ATTACKER or status == Status.ADDING):
        return context.table.hasRank(card.rank)
    if status == Status.DEFENDING:
        last = context.table.showLastDown()
        return (last.suit == card.suit and last.rank < card.rank or 
                not last.suit == card.suit and card.suit == context.stock.trump)

# PARAM IN:
#   status of actv player (which threw card)
#   table is object with actual state of table
#   rival_vol is number of cards in rival's hand
# PARAM OUT:
#   answer: can card be thrown to table
def canCardBeThrown(context: Context) -> bool:
    # 6*2 = 12 cards on table => ATTACKER should say BEATEN
    # or DEFENDING player do not have cards
    # number of cards added by ADDING player on table equals 
    # number of taking player's cards => ADDING should say TAKE_AWAY
    if ((context.players.actv.status == Status.ATTACKER or 
         context.players.actv.status == Status.ADDING) and 
        ((context.table.vol('down') - context.table.vol('up')) == context.players.pssv.vol or 
          context.table.vol('down') == CARDS_KIT)):
            return False
    return True


def isMoveCorrect(move, context: Context) -> bool:
    if 'card' in move:
        card = move.get('card')
        return (doesCardFit(card, context) and 
                canCardBeThrown(context))
    if 'word' in move:
        word = move.get('word')
        return not (word == Word.BEATEN and
                    context.table.vol == 0 and 
                    context.players.actv.status == Status.ATTACKER)
    return False


## UPDATING GAME CONTEXT AFTER PLAYER'S MOVE

def reactToWord(word: Word, context: Context) -> None:
    if word == Word.BEATEN:
        context.table.shift(context.deck)
        # context.players.actv.status = Status.DEFENDING
        context.players.pssv.status = Status.ATTACKER
        complete(context)
        context.players.swapRoles()
    if word == Word.TAKE:
        context.players.pssv.status = Status.ADDING
        context.players.swapRoles()
    if word == Word.TAKE_AWAY:
        context.table.shift(context.players.pssv)
        # context.players.actv.status  = Status.ATTACKER
        context.players.pssv.status = Status.DEFENDING
        complete(context)
    return gameIsOver(context)


# updating context by reaction to a active player's move
def reactToMove(move, context: Context) -> None:
    game_stage = GameStage.PLAYING
    if 'card' in move:
        card = move.get('card')
        atop = context.players.actv.status == Status.DEFENDING
        context.table.addCard(card, atop)
        if not context.players.actv.status == Status.ADDING:
            context.players.swapRoles()
    if 'word' in move:
        word = move.get('word')
        game_stage = reactToWord(word, context)
    return game_stage


## REPRESENTING OF RESULT OF THE GAME

def gameIsOver(context: Context) -> GameStage:
    stock_vol = context.stock.vol
    p1_vol    = context.players.actv.vol
    p2_vol    = context.players.pssv.vol
    if stock_vol == 0 and (p1_vol == 0 or p2_vol == 0):        
        return GameStage.GAME_OVER
    else:
        return GameStage.PLAYING


def whoIsFool(players: Players) -> int:
    actv_vol    = players.actv.vol
    pssv_vol    = players.pssv.vol
    # DEAD HEAT
    if actv_vol == 0 and pssv_vol == 0:
        fool_id = -1
    elif pssv_vol == 0:
        fool_id = players.getIdByRole('actv')
    elif actv_vol == 0:
        fool_id = players.getIdByRole('pssv')
    else: # wrong call
        print('ERROR: wrong call of whoIsFool func!')
        return None
    players.setFoolStatus(fool_id)


