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


class Player(Pile):
    def __init__(self, name: str):
        super().__init__()
        # main params        
        self.name = name
        self.status = None
                
        # game params
        self.trump = None
        self.__get_weight = lambda card : ((card.suit == self.trump)*
                                           Rank.ACE.value + card.rank.value)
    
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
    
    def setNewGameParams(self, trump: Suit, pl_1st: int):
        if not self._refs['actv'] == pl_1st:
            self.swapRoles()
        self.actv.setNewGameParams(trump, Status.ATTACKER)
        self.pssv.setNewGameParams(trump, Status.DEFENDING)
    
    def setFoolStatus(self, fool_id: int) -> None:
        if fool_id == 0 or fool_id == 1:
            fool = self.getPlayerById(fool_id)
            fool.status = Status.FOOL
            
    
# # TODO: class for playing with 3 players
# #class PlayersThreesome
