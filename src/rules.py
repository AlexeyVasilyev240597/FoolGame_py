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


# now in first game first move is given to first player (by order),
#     if dead heat then to player which throws last card 
#     and to winner otherwise
def deal(context: Context, winner_id: int = 0):
    context.deck.shuffle()
    trump = context.stock.setTrump()
    context.players.setNewGameParams(trump, winner_id)
    context.deck.shift(context.players.actv, CARDS_KIT)
    context.deck.shift(context.players.pssv, CARDS_KIT)


# TODO: describe according to the rules
def complete(context: Context):
    actv_add, pssv_add = context.players.howManyToComplete(context.stock.vol)
    # firstly cards are adding to passive player
    context.deck.shift(context.players.pssv, pssv_add)
    # then to active one
    context.deck.shift(context.players.actv, actv_add)


# collecting cards from all elements back to deck,
# call in finish of Game
def collect(context: Context):
    context.players.actv.shift(context.deck)
    context.players.pssv.shift(context.deck)


## CHECKING PLAYER'S MOVE FUNCTIONS

# PARAM INPUT:
#   card (thrown)
#   game context
# PARAM OUT:
#   answer: is chosen card correct
def doesCardFit(card: Card, context: Context) -> bool:
    status = context.players.actv.status
    if (status == Status.ATTACKER and
        context.table.vol == 0):
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
                canCardBeThrown(card, context))
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
    p1_vol    = players.actv.vol
    p2_vol    = players.pssv.vol
    if p1_vol == 0 and p2_vol == 0:
        # return players.getIdByRole('actv')
        return -1
    elif p2_vol == 0:
        players.actv.iAmFool()
        return players.pssv.name
    elif p1_vol == 0:
        players.pssv.iAmFool()
        return players.pssv.name
    else: # wrong call
        return None

