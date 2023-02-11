from enum import IntEnum

from .card    import Card
from .context import Context
# fro.m game_exception import WrongInitException
from .player  import Status, Word, Players


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
    CARD_EXPECTED     = 7
    
    

# TODO: add
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
    context.deck.shuffle()
    context.deck.shift(context.players.actv, CARDS_KIT)
    context.deck.shift(context.players.pssv, CARDS_KIT)
    context.deck.shift(context.stock)
    trump = context.stock.setTrump()
    context.players.setNewGameParams(trump, context.players.fool_id)


# TODO: describe according to the rules
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
        if not (last.suit == card.suit and last.rank.int() < card.rank.int() or 
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
    if 'card' in move:
        card = move.get('card')
        if not isinstance(card, Card):
            return MoveType.UNKNOWN_TYPE
        if not card in context.players.actv.cards:
            return MoveType.SHARPIE
        if not (move_type := doesCardFit(card, context)) == MoveType.CORRECT_MOVE:
            return move_type
        if not (move_type := canCardBeThrown(context)) == MoveType.CORRECT_MOVE:
            return move_type
        return MoveType.CORRECT_MOVE
            
    if 'word' in move:
        word = move.get('word')
        if not isinstance(word, Word):
            return MoveType.UNKNOWN_TYPE
        status = context.players.actv.status
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

def reactToWord(word: Word, context: Context) -> None:
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
    return gameIsOver(context)


# updating context by reaction to a active player's move
def reactToMove(move: dict, context: Context) -> None:
    game_stage = GameStage.PLAYING
    if 'card' in move:
        # some module outside should check if the move is correct!
        card_indx = context.players.actv.cards.index(move.get('card'))
        card = context.players.actv.getCard(card_indx)
        if context.players.actv.status == Status.DEFENDING:
            context.table.top.addCard(card)
        # Status.ATTACKER or Status.ADDING
        else:
            context.table.low.addCard(card)
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


def whoIsFool(players: Players):
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
    return fool_id


