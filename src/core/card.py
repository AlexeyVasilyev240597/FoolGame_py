from enum import IntEnum, Enum, Flag

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

class Side(Flag):
    BACK = 0
    FACE = 1

DECK_VOLUME = len(Rank)*len(Suit)


class Card:
    def __init__(self, suit: Suit, rank: Rank, side: Side = Side.BACK):
        self._suit = suit
        self._rank = rank
        self._side = side

    @property
    def suit(self):
        if self.open:
            return self._suit
        else:
            return None
    
    @property
    def rank(self):
        if self.open:
            return self._rank
        else:
            return None

    @property
    def open(self):
        if self._side == Side.BACK:
            return False
        else:
            return True
    
    def flip(self):
        self._side = Side(not self._side)
    
    def hide(self):
        if self.open:
            self.flip()
        self._rank = None
        self._side = None

    def __eq__(self, __o: object) -> bool:
        return self.open and self.suit == __o.suit and self.rank == __o.rank

    def __repr__(self):
        if self.side == Side.FACE:
            if self.rank.value == Rank.JACK:
                rank = 'J'
            elif self.rank.value == Rank.QUEEN:
                rank = 'Q'
            elif self.rank.value == Rank.KING:
                rank = 'K'
            elif self.rank.value == Rank.ACE:
                rank = 'A'
            else:
                rank = str(self.rank.value)
            return repr(rank + '-' + self.suit.value)
        else:
            # unknown
            return repr('UNK')