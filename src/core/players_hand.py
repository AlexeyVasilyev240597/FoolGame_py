from abc  import ABC
from enum import IntEnum

from src.core.card    import Rank, Suit, Card
from src.core.elems   import Pile


class Status(IntEnum):
    ATTACKER  = 1
    DEFENDING = 2
    ADDING    = 3
    FOOL      = 4

class Word(IntEnum):
    BEATEN    = 1
    TAKE      = 2
    TAKE_AWAY = 3
    # LOST      = 4
    # GIVE_IN   = 5


class PlayersHand(Pile):
    def __init__(self):
        super().__init__()
        # main params
        self.status = None
                
        # game params
        self.trump = None
    
    def addCard(self, card: Card) -> None:
        super().addCard(card)
        self.sortHand()
    
    def _get_weight(self, card):
        if card.open:
            return (card.suit == self.trump)*Rank.ACE.value + card.rank.value
        else:
            return 0
    
    # def _get_weight(self, card: Card):
    #     w = len(Rank)
    #     if not card.suit == self.trump:
    #         if card.suit == Suit.SPADES:
    #             w *= 0
    #         elif card.suit == Suit.HEARTS:
    #             w *= 1
    #         elif card.suit == Suit.DIAMONDS:
    #             w *= 2
    #         elif card.suit == Suit.CLUBS:
    #             w *= 3
    #     else:
    #         w *= 4
    #     w += card.rank.value - Rank.SIX.value
    #     return w
    
    def flipCards(self):
        [card.hide() for card in self.cards]
        
    def sortHand(self):
        self.cards.sort(key = self._get_weight)
    
    def setNewGameParams(self, trump, status):
        self.trump  = trump        
        self.status = status
        self.sortHand()
    

# structure for working with two players
class PlayersHands(ABC):
    def __init__(self, pl_1: PlayersHand, pl_2: PlayersHand) -> None:
        self._players = [pl_1, pl_2]
        self._refs = {'actv': 0,
                      'pssv': 1}

    @property
    def actv(self):
        return self._players[self._refs['actv']]
    
    @property
    def pssv(self):
        return self._players[self._refs['pssv']]

    def swapRoles(self):
        self._refs['actv'], self._refs['pssv'] = self._refs['pssv'], self._refs['actv']
    
    def getPlayerById(self, id: int) -> PlayersHand:
        if id == 0 or id == 1:
            return self._players[id]
        else:
            return None
    
    def getIdByRole(self, role: str) -> int:
        if role == 'actv' or role == 'pssv':
            return self._refs[role]
        else:
            return None
            
    
# # TODO: class for playing with 3 players
# #class PlayersThreesome
