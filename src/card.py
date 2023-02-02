from enum import IntEnum, Enum

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

#[ '\u2660', '\u2665', '\u2666', '\u2663' ]
class Suit(Enum):
    SPADES   = 'S'
    HEARTS   = 'H'
    DIAMONDS = 'D'
    CLUBS    = 'C'

DECK_VOLUME = len(Rank)*len(Suit)


class Card:        
    def __init__(self, suit: Suit, rank: Rank):        
        self.suit = suit
        self.rank = rank

    def __eq__(self, __o: object) -> bool:
        return self.suit == __o.suit and self.rank == __o.rank

    def __repr__(self):
        if self.rank < Rank.JACK.value:
            r = str(self.rank.value)
        else:
            r = self.rank.name[0]
        # r = str(self.rank.value)
        return f'{self.suit.value} - {r:<2}'
