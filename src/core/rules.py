from enum import IntEnum

from src.core.card    import Card
from src.core.context import Context
from src.core.player  import Status, Word
# from game_exception import WrongInitException


CARDS_KIT = 6

class GameStage(IntEnum):
    START     = 1
    PLAYING   = 2
    GAME_OVER = 3
    
class MoveType(IntEnum):
    CORRECT_MOVE      = 0
    # the move is neither a card, nor a word
    UNKNOWN_TYPE      = 1
    # player threw a card that is not in his hand
    SHARPIE           = 2
    # ATTACKER and ADDING shall trow card with ranks which already are on the table
    NO_SUCH_RANK      = 3
    # DEFENDING shall trow card with more weight than last thrown one is
    LIGHTER_THAN_LAST = 4
    # there is no more space on the table (6 pair or rival wouldn't be able to beat that much)
    NO_MORE_SPACE     = 5
    # the word doesn't correspond the status of player
    WRONG_WORD        = 6
    # it was expected a card instead of a word
    CARD_EXPECTED     = 7,
    # when fool must say that he/she lose
    WORD_EXPECTED     = 8
    
    

class ResultOfRaund(IntEnum):
    NEW_GAME    = 0
    FOOL_EXISTS = 1
    DEAD_HEAT   = 2


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


def whoseFirstMove(prev_result: tuple) -> None:
    # in first round the first move is given to first player (by order)
    if prev_result[0] == ResultOfRaund.NEW_GAME:
        pl_1st = 0
    # if dead heat then to player which throws last card
    # and to winner otherwise
    elif (prev_result[0] == ResultOfRaund.DEAD_HEAT or
          prev_result[0] == ResultOfRaund.FOOL_EXISTS):
        pl_1st = int(not prev_result[1])
    else:
        return None
    return pl_1st

# now in first game first move is given to first player (by order),
#     if dead heat then to player which throws last card 
#     and to winner otherwise
def deal(context: Context):
    # TODO: uncommnet this line - just for debugging comment
    context.deck.shuffle()
    context.deck.shift(context.players.actv, CARDS_KIT)
    context.deck.shift(context.players.pssv, CARDS_KIT)
    context.deck.shift(context.stock)
    context.stock.setTrump()


def complete(context: Context):
    actv_add, pssv_add = howManyToComplete(context)
    # firstly cards are adding to passive player
    context.stock.shift(context.players.pssv, pssv_add)
    # then to active one
    context.stock.shift(context.players.actv, actv_add)


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
def doesCardFit(card: Card, context: Context) -> MoveType:
    status = context.players.actv.status
    if status == Status.ATTACKER and context.table.low.vol == 0:
        return MoveType.CORRECT_MOVE
    if status == Status.ATTACKER or status == Status.ADDING:
        if not context.table.hasRank(card.rank):
            return MoveType.NO_SUCH_RANK
    if status == Status.DEFENDING:
        last = context.table.showLastDown()
        trump = context.stock.trump
        if not (last.suit == card.suit and last.rank.value < card.rank.value or 
                not last.suit == trump and card.suit == trump):
            return MoveType.LIGHTER_THAN_LAST
    return MoveType.CORRECT_MOVE

# PARAM IN:
#   game context
# PARAM OUT:
# is there enough space on the table?
# MoveType.CORRECT_MOVE if so
# MoveType.NO_MORE_SPACE otherwise
def canCardBeThrown(context: Context) -> MoveType:
    # 6*2 = 12 cards on table => ATTACKER should say BEATEN
    # or DEFENDING player do not have cards
    # number of cards added by ADDING player on table equals 
    # number of taking player's cards => ADDING should say TAKE_AWAY
    if ((context.players.actv.status == Status.ATTACKER or 
         context.players.actv.status == Status.ADDING) and 
        ((context.table.low.vol - context.table.top.vol) == 
          context.players.pssv.vol or 
          context.table.low.vol == CARDS_KIT)):
            return MoveType.NO_MORE_SPACE
    return MoveType.CORRECT_MOVE


def isMoveCorrect(move, context: Context) -> MoveType:
    status = context.players.actv.status
    if 'card' in move:
        card = move.get('card')
        if not isinstance(card, Card):
            return MoveType.UNKNOWN_TYPE
        if status == Status.FOOL:
            return MoveType.WORD_EXPECTED
        if not card in context.players.actv.cards:
            return MoveType.SHARPIE
        if not ((move_type := doesCardFit(card, context)) == 
                MoveType.CORRECT_MOVE):
            return move_type
        if not ((move_type := canCardBeThrown(context)) == 
                MoveType.CORRECT_MOVE):
            return move_type
        return MoveType.CORRECT_MOVE
            
    if 'word' in move:
        word = move.get('word')
        if not isinstance(word, Word):
            return MoveType.UNKNOWN_TYPE
        if (word == Word.BEATEN and not status == Status.ATTACKER):
            return MoveType.WRONG_WORD
        if (word == Word.TAKE and not status == Status.DEFENDING):
            return MoveType.WRONG_WORD
        if (word == Word.TAKE_AWAY and not status == Status.ADDING):
            return MoveType.WRONG_WORD
        if (word == Word.BEATEN and
            context.table.low.vol == 0 and status == Status.ATTACKER):
            return MoveType.CARD_EXPECTED
        return MoveType.CORRECT_MOVE
    return MoveType.UNKNOWN_TYPE



## UPDATING GAME CONTEXT AFTER PLAYER'S MOVE

def react2Word(word: Word, context: Context) -> None:
    if word == Word.BEATEN:
        context.table.shift(context.deck)
        context.players.actv.status = Status.DEFENDING
        context.players.pssv.status = Status.ATTACKER
        complete(context)
        context.players.swapRoles()
    if word == Word.TAKE:
        context.players.pssv.status = Status.ADDING
        context.players.swapRoles()
    if word == Word.TAKE_AWAY:
        context.table.shift(context.players.pssv)
        context.players.actv.status  = Status.ATTACKER
        # status stays still the same
        # context.players.pssv.status = Status.DEFENDING
        complete(context)


# updating context by reaction to a active player's move
def react2Move(move: dict, context: Context) -> None:
    if 'card' in move:
        # some module outside should check if the move is correct!
        card_indx = context.players.actv.cards.index(move.get('card'))
        if context.players.actv.status == Status.DEFENDING:
            table_layer = context.table.top
        # Status.ATTACKER or Status.ADDING
        else:
            table_layer = context.table.low
        context.players.actv.swop(table_layer, card_indx)
        if not context.players.actv.status == Status.ADDING:
            context.players.swapRoles()
    if 'word' in move:
        word = move.get('word')
        react2Word(word, context)
    context.last_move = move


## REPRESENTING OF RESULT OF THE GAME

def gameIsOver(context: Context) -> GameStage:
    if 'word' in context.last_move:
        stock_vol = context.stock.vol
        p1_vol    = context.players.actv.vol
        p2_vol    = context.players.pssv.vol
        if stock_vol == 0 and (p1_vol == 0 or p2_vol == 0):        
            return GameStage.GAME_OVER
    return GameStage.PLAYING


def whoIsFool(context: Context):
    players  = context.players
    actv_vol = players.actv.vol
    actv_id  = players.getIdByRole('actv')
    pssv_vol = players.pssv.vol
    pssv_id  = players.getIdByRole('pssv')
    
    # DEAD HEAT
    if actv_vol == 0 and pssv_vol == 0:
        result = [ResultOfRaund.DEAD_HEAT, pssv_id]
    else:
        if pssv_vol == 0:
            fool_id = actv_id
        elif actv_vol == 0:
            fool_id = pssv_id    
        else: # wrong call
            print('ERROR: wrong call of whoIsFool func!')
            return None
        result = [ResultOfRaund.FOOL_EXISTS, fool_id]
    return result


