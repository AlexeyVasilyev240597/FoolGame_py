from enum import Enum

class Rank(Enum):
    SIX   = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE  = '9'
    TEN   = '10'
    JACK  = 'J'
    QUEEN = 'Q'
    KING  = 'K'
    ACE   = 'A'

    def int(self):
        if self.value == 'J':
            return 11
        elif self.value == 'Q':
            return 12
        elif self.value == 'K':
            return 13
        elif self.value == 'A':
            return 14
        else:
            return int(self.value)

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
        # return f'{self.suit.value}-{self.rank.value:<2}'
        return f'{self.rank.value:>2}-{self.suit.value}'
