from enum import IntEnum, Enum

class Suit(Enum):
    SPADES   = 'S'
    HEARTS   = 'H'
    DIAMONDS = 'D'
    CLUBS    = 'C'

class Rank(IntEnum):
    SIX   = 6
    SEVEN = 7
    EIGHT = 8
    NINE  = 9
    TEN   = 10
    JACK  = 11
    QUEEN = 12
    KING  = 13
    ACE   = 14

DECK_VOLUME = len(Rank)*len(Suit)


class Card:
    # if both arguments are None then the card is face down
    def __init__(self, suit: Suit = None, rank: Rank = None):
        if suit == None and rank == None:
            self.open = False
        else:
            self.open = True
        self.suit = suit
        self.rank = rank

    def __eq__(self, __o: object) -> bool:
        return self.open and self.suit == __o.suit and self.rank == __o.rank

