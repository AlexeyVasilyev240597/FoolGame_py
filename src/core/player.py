from abc  import ABC
from enum import IntEnum

from .card    import Rank, Suit, Card
from .elems   import Pile


class Status(IntEnum):
    ATTACKER  = 1
    DEFENDING = 2
    ADDING    = 3
    FOOL      = 4

class Word(IntEnum):
    BEATEN    = 1
    TAKE      = 2
    TAKE_AWAY = 3
    LOST      = 4
    # GIVE_IN   = 5


class Player(Pile):
    def __init__(self, name: str):
        super().__init__()
        # main params        
        self.name = name
        self.status = None
                
        # game params
        self.trump = None
        self.__get_weight = lambda card : ((card.suit == self.trump)*
                                          Rank.ACE.int() +
                                          card.rank.int())
    
    def addCard(self, card: Card) -> None:
        super().addCard(card)
        # in case if card is None
        if card:
            self.cards.sort(key = self.__get_weight)
    
    def setNewGameParams(self, trump, status):
        self.trump  = trump        
        self.status = status
        self.cards.sort(key = self.__get_weight)
    

# structure for working with two players
class Players(ABC):
    def __init__(self, pl_1: Player, pl_2: Player) -> None:
        self._players = [pl_1, pl_2]
        self._refs = {'actv': 0,
                      'pssv': 1}
        self.fool_id = -1

    @property
    def actv(self):
        return self._players[self._refs['actv']]
    
    @property
    def pssv(self):
        return self._players[self._refs['pssv']]

    def swapRoles(self):
        self._refs['actv'], self._refs['pssv'] = self._refs['pssv'], self._refs['actv']
    
    def getPlayerById(self, id: int) -> Player:
        if id == 0 or id == 1:
            return self._players[id]
        else:
            return None
    
    def getIdByRole(self, role: str) -> int:
        if role == 'actv' or role == 'pssv':
            return self._refs[role]
        else:
            return None
    
    # now in first game first move is given to first player (by order),
    #     if dead heat then to player which throws last card 
    #     and to winner otherwise
    # TODO: make rules above more explicit in the code
    def setNewGameParams(self, trump: Suit, fool_id):
        if self._refs['actv'] == fool_id or fool_id == -1:
            self.swapRoles()
        self.actv.setNewGameParams(trump, Status.ATTACKER)
        self.pssv.setNewGameParams(trump, Status.DEFENDING)
    
    def setFoolStatus(self, fool_id: int) -> None:
        self.fool_id = fool_id
        if fool_id == 0 or fool_id == 1:
            fool = self.getPlayerById(fool_id)
            fool.status = Status.FOOL
            
    
# # TODO: class for playing with 3 players
# #class PlayersThreesome
