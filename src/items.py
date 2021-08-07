from enum import IntEnum, Enum, Flag

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

#['\u2666', '\u2663', '\u2665', '\u2660']
class Suit(Enum):
    DIAMONDS = 'D'
    HEARTS   = 'H'
    CLUBS    = 'C'
    SPADES   = 'S'

DECK_VOLUME = len(Rank)*len(Suit)
    
class Side(Flag):
    BACK = 0
    FACE = 1

class Card:        
    def __init__(self, suit, rank):        
        self.suit = suit
        self.rank = rank         
        self.side = Side.BACK

    def __repr__(self):
        if self.side == Side.FACE:
            # return repr(self.rank.name + ' of ' + self.suit.name)
            if self.rank < Rank.JACK.value:
                r = str(self.rank.value)
            else:
                r = self.rank.name[0]
            return repr(self.suit.value + '-' + r)
        else:
            return repr('*-*')

    def flip(self):
        self.side = Side(not self.side)