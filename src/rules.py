from params import MAGIC_CONST
from player import Status

def isChoiceCorrect(status, table, card, trump):
    if table.vol() == 0:
        return True
    if status == Status.ATTACKER or status == Status.ADDING:
        for c in table.cards.sprites():
            if card.rank == c.rank:
                return True
        return False
    if status == Status.DEFENDING:
        last = table.cards.sprites()[-1]
        return last.suit == card.suit and last.rank < card.rank or not last.suit == card.suit and card.suit == trump

# TODO: rewrite with switch by all Status values 
# and check last case because there is BUG!
#def canCardBeThrown(players, table):
def canCardBeThrown(status, table, rival_vol):
    # 6*2 = 12 cards on table => ATTACKER should say BEATEN
    # or DEFENDING player do not have cards
    if table.last_down == MAGIC_CONST:
        return False
    # number of cards added by ADDING player on table equals 
    # number of TAKING player's cards => ADDING should say TAKE_AWAY
    if status == Status.ADDING:
        if (table.last_down - table.last_up) == rival_vol:
            return False
    return True
